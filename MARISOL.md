# MARISOL.md — Pipeline Context

## Project Overview
piDSLM is a Raspberry Pi DSLR-like camera interface project that provides a GUI for controlling a Raspberry Pi HQ Camera with GPIO controls. The application uses guizero for the GUI framework and RPi.GPIO for hardware control, with picamera for camera operations. It supports photo capture, video recording, and Dropbox uploads.

## Build & Run
- **Language**: Python 3.x
- **Framework**: guizero (GUI), picamera (camera), RPi.GPIO (hardware control)
- **Docker image**: python:3.12-slim (base image; requires hardware mocking for RPi modules)
- **Install deps**: pip install -r requirements.txt
- **Run**: python3 pidslm.py (requires Raspberry Pi hardware; in container, use mocked environment via conftest.py)

## Testing
- **Test framework**: pytest
- **Test command**: python3 -m pytest tests/ -v
- **Hardware mocks needed**: yes — conftest.py mocks RPi.GPIO, picamera, guizero, spidev, smbus, gpiozero, and 15+ other hardware modules
- **Known test issues**: Tests require conftest.py to mock hardware modules; without mocks, tests will fail on non-RPi systems

## Pipeline History
- Initial setup: Verified guizero and picamera dependencies in requirements.txt
- Test infrastructure: conftest.py provides comprehensive hardware mocking for pytest
- Source analysis: pidslm.py uses guizero App, PushButton, Text, Picture, Window components
- Hardware integration: RPi.GPIO for GPIO control, picamera for camera operations

## Known Issues
- No runnable entry point in standard Docker containers without hardware mocking
- Tests require conftest.py to mock RPi hardware modules (RPi.GPIO, picamera, guizero, etc.)
- GUI application requires Raspberry Pi hardware or mocked environment

## Notes
- **Main entry point**: pidslm.py (standalone application with while-True loop for GUI)
- **Dropbox integration**: dropbox_upload.py for cloud storage
- **Hardware mocks**: tests/embedded_mocks.py includes MockGPIO, MockI2C, MockSPI, MockUART (referenced in conftest.py)
- **Dependencies**: Pillow, guizero, dropbox, guizero[images]
- **Installation script**: INSTALL.sh (requires sudo for hardware setup)
- **Mocking strategy**: conftest.py uses AST parsing to strip while-True loops from source files before loading
