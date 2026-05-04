# EasyChords : Play Piano Chords from Any Scale at the Press of a Button
A standalone, offline Windows desktop application that allows users to explore musical scales and play piano chords interactively. Built with a Python backend and a responsive web-based frontend, the application generates real-time audio and is packaged as a zero-dependency executable.

## ✨ Features
**Offline Functionality**: Runs natively on Windows without requiring an internet connection.

**Scale Selection**: Users can choose from musical scales, dynamically calculating the appropriate notes and degrees (e.g., Major and Minor scales with their respective I, ii, iii, etc., degrees).

**Interactive Playback**: Clicking a chord button plays the corresponding piano chord audio. The sound continues for as long as the button is pressed.

**Custom Audio Synthesis**: Generates audio natively using mathematical waveforms with harmonic amplitudes and an Attack-Decay-Sustain-Release (ADSR) envelope for a realistic piano-like resonance.

**Custom Sustain Control**: Features an adjustable sustain setting, allowing users to define how long the chord fades out after the button is released.

**Zero-Dependency Executable**: Compiled into a single .exe with an embedded custom circular icon for seamless distribution.

## 🛠️ Technology Stack
**Frontend**: HTML, CSS, JavaScript (served from a local web/ directory).

**Backend**: Python.

**Core Libraries**:

  *Eel (v0.18.2)*: Facilitates the communication between the Python backend and the JavaScript frontend.  

  *Pygame (v2.6.1)*: Handles the initialization of the audio mixer and the low-latency playback of the audio arrays.  

  *NumPy (v2.2.4)*: Drives the heavy lifting of calculating frequencies and generating the multi-harmonic sine waves for the audio chords.  

  *Pillow (PIL)*: Used in the build pipeline to generate high-quality, transparent circular .ico and .png assets from source images.

## 🗂️ Project Structure
**offline_chords.py**: The main entry point. It contains the core mathematical logic for MIDI-to-frequency conversion, scale building, and the generate_waveform function that builds the audio using NumPy.

**chord_ui.py**: The bridging layer. It initializes Eel, exposes Python functions (like set_sustain, start_chord, and stop_chord) to the JavaScript frontend, and manages the Pygame sound objects.

**make_circular_icon.py & convert_to_ico.py**: Utility scripts that crop a source image into a high-quality circular mask and export it as a multi-resolution .ico file for the Windows executable.

**requirements.txt**: Lists the core dependencies required to run the application (numpy, pygame, eel).  

## 🚀 Getting Started (For Users)
**Installation**

Navigate to the Releases tab of this repository.

Download the latest .exe file.

Double-click the downloaded executable to launch the application. No installation wizard or additional dependencies are required.

## 💻 Development Setup (For Developers)
If you wish to clone this repository and run or build the application from the source code, follow these steps:

**Prerequisites**

Python 3.11+ installed on your machine.

**Running Locally**

Clone the repository:

**Bash**

clone https://github.com/4sameek4/EasyChords.git
cd piano-chord-generator

## Install the required dependencies:
**Bash**

pip install -r requirements.txt


## Run the main application:
**Bash**

python offline_chords.py

**Windows**

Run EasyChords.exe

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📝 License
This project is licensed under the MIT License. Note that this software relies on NumPy, which is distributed under the BSD 3-Clause License.
