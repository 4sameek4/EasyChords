// script.js
let currentScaleRoot = 'C';
let currentScaleType = 'Major';
let noteNames = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
let degreeLabels = {
    "Major": ["I", "ii", "iii", "IV", "V", "vi", "vii°"],
    "Minor": ["i", "ii°", "III", "iv", "v", "VI", "VII"]
};
let sustainEnabled = false;
let sustainValue = 0;

document.addEventListener('DOMContentLoaded', function() {
    updateDisplay();
    setupEventListeners();
});

function setupEventListeners() {
    // Scale controls
    document.getElementById('scale-below').addEventListener('click', scaleBelow);
    document.getElementById('set-scale').addEventListener('click', openScaleModal);
    document.getElementById('scale-above').addEventListener('click', scaleAbove);

    // Modal
    document.getElementById('confirm-scale').addEventListener('click', confirmScale);
    document.querySelector('.close').addEventListener('click', closeScaleModal);
    window.addEventListener('click', function(event) {
        if (event.target == document.getElementById('scale-modal')) {
            closeScaleModal();
        }
    });

    // Populate root select
    const rootSelect = document.getElementById('root-select');
    noteNames.forEach(note => {
        const option = document.createElement('option');
        option.value = note;
        option.textContent = note;
        rootSelect.appendChild(option);
    });

    const sustainToggle = document.getElementById('sustain-toggle');
    const sustainSlider = document.getElementById('sustain-slider');
    const sustainValueLabel = document.getElementById('sustain-value');

    sustainToggle.addEventListener('click', () => {
        sustainEnabled = !sustainEnabled;
        sustainToggle.classList.toggle('active', sustainEnabled);
        sustainToggle.textContent = sustainEnabled ? 'Sustain: On' : 'Sustain: Off';
        setSustain();
    });

    sustainSlider.addEventListener('input', () => {
        sustainValue = parseInt(sustainSlider.value, 10);
        sustainValueLabel.textContent = sustainValue;
        if (sustainEnabled) {
            setSustain();
        }
    });

    sustainValueLabel.textContent = sustainValue;
}

function updateDisplay() {
    // Update scale info
    const aboveRoot = noteNames[(noteNames.indexOf(currentScaleRoot) + 1) % 12];
    const belowRoot = noteNames[(noteNames.indexOf(currentScaleRoot) - 1 + 12) % 12];
    document.getElementById('scale-info').textContent =
        `Scale below: ${belowRoot} ${currentScaleType} | Current: ${currentScaleRoot} ${currentScaleType} | Scale above: ${aboveRoot} ${currentScaleType}`;

    // Update chord buttons
    const chordButtons = document.getElementById('chord-buttons');
    chordButtons.innerHTML = '';
    const labels = degreeLabels[currentScaleType];
    for (let degree = 0; degree < 7; degree++) {
        const button = document.createElement('button');
        button.className = 'chord-button';
        button.setAttribute('data-degree', degree);
        button.textContent = `${labels[degree]}: Loading...`;
        button.addEventListener('mousedown', () => startChord(degree));
        button.addEventListener('mouseup', stopChord);
        button.addEventListener('mouseleave', stopChord);
        chordButtons.appendChild(button);
    }

    // Update with actual chords from Python
    if (typeof eel !== 'undefined') {
        eel.get_chords()(function(chords) {
            const buttons = chordButtons.querySelectorAll('.chord-button');
            chords.forEach((chord, index) => {
                if (buttons[index]) {
                    buttons[index].textContent = chord.name;
                }
            });
        });
    } else {
        setTimeout(updateDisplay, 100);
    }
}

function startChord(degree) {
    if (typeof eel !== 'undefined') {
        eel.start_chord(degree)();
    }
}

function stopChord() {
    if (typeof eel !== 'undefined') {
        eel.stop_chord()();
    }
}

function scaleBelow() {
    const currentIndex = noteNames.indexOf(currentScaleRoot);
    currentScaleRoot = noteNames[(currentIndex - 1 + 12) % 12];
    if (typeof eel !== 'undefined') {
        eel.set_scale(currentScaleRoot, currentScaleType);
    }
    updateDisplay();
}

function scaleAbove() {
    const currentIndex = noteNames.indexOf(currentScaleRoot);
    currentScaleRoot = noteNames[(currentIndex + 1) % 12];
    if (typeof eel !== 'undefined') {
        eel.set_scale(currentScaleRoot, currentScaleType);
    }
    updateDisplay();
}

function openScaleModal() {
    document.getElementById('root-select').value = currentScaleRoot;
    document.getElementById('type-select').value = currentScaleType;
    document.getElementById('scale-modal').style.display = 'block';
}

function closeScaleModal() {
    document.getElementById('scale-modal').style.display = 'none';
}

function confirmScale() {
    currentScaleRoot = document.getElementById('root-select').value;
    currentScaleType = document.getElementById('type-select').value;
    if (typeof eel !== 'undefined') {
        eel.set_scale(currentScaleRoot, currentScaleType);
    }
    updateDisplay();
    closeScaleModal();
}

function setSustain() {
    if (typeof eel !== 'undefined') {
        const sustainSeconds = sustainEnabled ? sustainValue / 2 : 0;
        eel.set_sustain(sustainSeconds);
    }
}

// Eel functions to update status
if (typeof eel !== 'undefined') {
    eel.expose(update_status);
}
function update_status(message) {
    document.getElementById('status').textContent = message;
}