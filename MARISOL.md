# MARISOL.md — Pipeline Context

## Project Overview
Raspberry Pi-based blind control system using stepper motors with Firebase/Alexa integration. The system controls window blinds through a state machine that responds to Alexa voice commands and Firebase updates. Hardware control is implemented using Python with GPIO pins for stepper motor control.

## Build & Run
- **Language**: Python 3.x
- **Framework**: None (custom implementation)
- **Docker image**: python:3.12-slim
- **Install deps**: pip install --no-cache-dir pytest fake-rpi Pillow 2>&1 | tail -3; pip install pytest 2>&1 | tail -3
- **Run**: python blindscontrol_controller_interface.py

## Testing
- **Test framework**: pytest
- **Test command**: python -m pytest tests/ -v
- **Hardware mocks needed**: yes (fake-rpi for RPi.GPIO, Pillow for image processing)
- **Known test issues**: None documented

## Pipeline History
- Initial pipeline setup with pytest and fake-rpi for hardware mocking
- Docker environment configured with python:3.12-slim
- Test PR created: https://github.com/NickEngmann/BlindsControl/pull/12

## Known Issues
- None documented

## Notes
- Project uses custom state machine pattern for blind control
- Alexa integration via Firebase Realtime Database
- GPIO control for stepper motors on Raspberry Pi
- No external dependencies beyond standard library, fake-rpi, and Pillow
