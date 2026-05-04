import eel
import numpy as np
import os
import sys
import pygame
from offline_chords import NOTE_NAMES, SCALE_STEPS, DEGREE_LABELS, build_scale, build_chord, midi_to_frequency, note_name_to_midi, generate_waveform, LOOP_DURATION


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)


eel.init(resource_path('web'))

current_sound = None
current_sustain = 0.0
scale_root = "C"
scale_type = "Major"
scale_notes = build_scale(scale_root, scale_type)

@eel.expose
def set_sustain(seconds):
    global current_sustain
    current_sustain = max(0.0, float(seconds))

@eel.expose
def start_chord(degree):
    global current_sound
    if current_sound:
        current_sound.stop()
    chord_root, chord_notes = build_chord(scale_notes, degree)
    midi_notes = [note_name_to_midi(note, 4) for note in chord_notes]
    frequencies = [midi_to_frequency(midi_note) for midi_note in midi_notes]
    audio = generate_waveform(frequencies, LOOP_DURATION, fade=True)

    mixer_init = pygame.mixer.get_init()
    if mixer_init is not None:
        channels = mixer_init[2]
    else:
        channels = 1

    if channels == 2 and audio.ndim == 1:
        audio = np.column_stack((audio, audio))

    current_sound = pygame.sndarray.make_sound(audio)
    current_sound.play()
    suffix = _chord_suffix(degree, scale_type)
    chord_name = f"{chord_root}{suffix}"
    eel.update_status(f"Playing chord: {chord_name} (Notes: {', '.join(chord_notes)})")

@eel.expose
def stop_chord():
    global current_sound
    if current_sound:
        if current_sustain > 0:
            current_sound.fadeout(int(current_sustain * 1000))
        else:
            current_sound.stop()
        current_sound = None
    eel.update_status("Choose a scale and press any chord.")

@eel.expose
def scale_changed():
    global current_sound
    if current_sound:
        current_sound.stop()
        current_sound = None
    eel.update_status(f"Selected scale: {scale_root} {scale_type}")

@eel.expose
def set_scale(root, type):
    global scale_root, scale_type, scale_notes
    scale_root = root
    scale_type = type
    scale_notes = build_scale(scale_root, scale_type)
    scale_changed()

@eel.expose
def get_scale_info():
    above_root = NOTE_NAMES[(NOTE_NAMES.index(scale_root) + 1) % len(NOTE_NAMES)]
    below_root = NOTE_NAMES[(NOTE_NAMES.index(scale_root) - 1) % len(NOTE_NAMES)]
    return {
        'below': f"{below_root} {scale_type}",
        'current': f"{scale_root} {scale_type}",
        'above': f"{above_root} {scale_type}"
    }

def _chord_suffix(degree: int, scale_type: str) -> str:
    if scale_type == "Major":
        suffixes = [" major", " minor", " minor", " major", " major", " minor", " diminished"]
    else:
        suffixes = [" minor", " diminished", " major", " minor", " minor", " major", " major"]
    return suffixes[degree]


@eel.expose
def get_chords():
    chords = []
    labels = DEGREE_LABELS[scale_type]
    for degree in range(7):
        chord_root, chord_notes = build_chord(scale_notes, degree)
        suffix = _chord_suffix(degree, scale_type)
        chord_name = f"{chord_root}{suffix}"
        chords.append({
            'label': labels[degree],
            'name': chord_name,
            'text': f"{chord_name} - {', '.join(chord_notes)}"
        })
    return chords
