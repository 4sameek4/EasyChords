import os
import sys
import numpy as np
import pygame

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SCALE_STEPS = {
    "Major": [2, 2, 1, 2, 2, 2, 1],
    "Minor": [2, 1, 2, 2, 1, 2, 2],
}
DEGREE_LABELS = {
    "Major": ["I", "ii", "iii", "IV", "V", "vi", "vii°"],
    "Minor": ["i", "ii°", "III", "iv", "v", "VI", "VII"],
}
SAMPLE_RATE = 44100
LOOP_DURATION = 10.0
DURATION_SECONDS = 5
VOLUME = 0.3


def midi_to_frequency(midi_note: int) -> float:
    return 440.0 * 2 ** ((midi_note - 69) / 12)


def note_name_to_midi(note_name: str, octave: int) -> int:
    note_name = note_name.strip().upper().replace("B#", "C").replace("E#", "F")
    if note_name in ["CB"]:
        note_name = "B"
        octave -= 1
    if note_name in ["FB"]:
        note_name = "E"
        octave -= 1

    if note_name not in NOTE_NAMES:
        raise ValueError(f"Unknown note name: {note_name}")

    note_index = NOTE_NAMES.index(note_name)
    return 12 * (octave + 1) + note_index


def build_scale(root: str, scale_type: str) -> list[str]:
    if scale_type not in SCALE_STEPS:
        raise ValueError(f"Unknown scale type: {scale_type}")

    root_index = NOTE_NAMES.index(root)
    steps = SCALE_STEPS[scale_type]
    scale = [root]
    current = root_index
    for step in steps[:-1]:
        current = (current + step) % 12
        scale.append(NOTE_NAMES[current])
    return scale


def build_chord(scale: list[str], degree: int) -> tuple[str, list[str]]:
    root_name = scale[degree]
    third_name = scale[(degree + 2) % len(scale)]
    fifth_name = scale[(degree + 4) % len(scale)]
    return root_name, [root_name, third_name, fifth_name]


def generate_waveform(frequencies: list[float], duration: float, fade: bool = True) -> np.ndarray:
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    waveform = np.zeros_like(t)
    harmonic_amplitudes = [1.0, 0.55, 0.35, 0.2, 0.12]
    for freq in frequencies:
        note_wave = np.zeros_like(t)
        for i, amp in enumerate(harmonic_amplitudes, start=1):
            note_wave += amp * np.sin(freq * t * 2 * np.pi * i)
        note_wave /= sum(harmonic_amplitudes)
        waveform += note_wave
    waveform /= max(len(frequencies), 1)

    attack = min(0.04, duration * 0.03)
    decay = min(0.08, duration * 0.06)
    sustain_level = 0.78
    release = min(0.8, duration * 0.18)
    env = np.zeros_like(t)

    for idx, time in enumerate(t):
        if time < attack:
            env[idx] = 0.5 + 0.5 * (time / attack)
        elif time < attack + decay:
            env[idx] = 1.0 - (1.0 - sustain_level) * ((time - attack) / decay)
        elif time < duration - release:
            env[idx] = sustain_level
        else:
            env[idx] = sustain_level * max(0.0, (duration - time) / release)

    if fade:
        edge_time = min(0.01, duration * 0.03)
        if edge_time > 0:
            edge_samples = max(1, int(SAMPLE_RATE * edge_time))
            env[:edge_samples] *= np.linspace(0.0, 1.0, edge_samples)
            env[-edge_samples:] *= np.linspace(1.0, 0.0, edge_samples)

    waveform *= env
    waveform *= VOLUME
    audio = np.int16(np.clip(waveform, -1.0, 1.0) * 32767)
    return audio


def play_notes(notes: list[str], octave: int = 4) -> None:
    midi_notes = [note_name_to_midi(note, octave) for note in notes]
    frequencies = [midi_to_frequency(midi_note) for midi_note in midi_notes]
    audio = generate_waveform(frequencies, DURATION_SECONDS)

    mixer_init = pygame.mixer.get_init()
    if mixer_init is not None:
        channels = mixer_init[2]
    else:
        channels = 1

    if channels == 2 and audio.ndim == 1:
        audio = np.column_stack((audio, audio))

    sound = pygame.sndarray.make_sound(audio)
    sound.play()
    pygame.time.wait(int(DURATION_SECONDS * 1000))


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    pygame.mixer.pre_init(SAMPLE_RATE, -16, 1, 512)
    pygame.mixer.init(SAMPLE_RATE, -16, 1, 512)
    pygame.init()
    import eel
    import chord_ui
    eel.start('index.html', size=(800, 600))
