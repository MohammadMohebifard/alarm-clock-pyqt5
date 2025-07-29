# PyQt5 Alarm Clock

A modern, fully functional alarm clock with GUI, built using PyQt5 and pygame.  
Supports audio selection, time tracking, and intuitive user experience.

---

## Features

- Real-time digital clock display
- Set and trigger alarm with custom sound
- Select MP3/WAV files for alarm
- PyQt5 GUI with intuitive interface
- Uses threads to avoid freezing the GUI

---

## How to Run

> It's recommended to use a virtual environment:

```bash
# Optional: Create a virtual environment
python -m venv env

# Activate the environment
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Then run the application:

```bash
python src/Alarm_Clock.py
```

---

## Requirements

Add this to your `requirements.txt` file:

```
pyqt5
pygame
```

Install with:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
alarm-clock-pyqt5/
├── src/
│   └── Alarm_Clock.py
├── assets/
│   └── (sound files here)
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## Author

Mohammad Mohebifard 
Released under the MIT License.
