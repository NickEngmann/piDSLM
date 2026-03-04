# MARISOL.md — Pipeline Context

## Project Overview
piDSLM is a Raspberry Pi DSLR-like camera interface project that provides GUI controls for photo/video capture using the HQ Camera, with Dropbox upload integration. The project uses Python with guizero for the GUI, RPi.GPIO for hardware control, and picamera/picamera2 for camera operations. It's designed for Raspberry Pi 2/3 with MHS35-TFT display.

## Build & Run
- **Language**: Python 3.x
- **Framework**: guizero (GUI framework)
- **Docker image**: python:3.12-slim
- **Install deps**: `pip install -r requirements.txt`
- **Run**: `python3 pidslm.py` (requires Raspberry Pi hardware with HQ Camera and MHS35-TFT display)

## Testing
- **Test framework**: pytest
- **Test command**: `python -m pytest tests/ -v`
- **Hardware mocks needed**: yes — RPi.GPIO, guizero, picamera, picamera2, gpiozero, spidev, and other hardware modules are pre-mocked in tests/conftest.py
- **Known test issues**: The main application (pidslm.py) contains while-True loops that prevent normal execution in headless environments; conftest.py strips these loops via AST parsing for testing

## Pipeline History
- Initial pipeline run: Project structure analyzed, dependencies verified
- Test setup verified: conftest.py provides 15+ RPi hardware module mocks
- Source loading: source_module fixture loads pidslm.py and dropbox_upload.py with hardware mocks active

## Known Issues
- **Hardware dependency**: Project requires actual Raspberry Pi hardware (HQ Camera, MHS35-TFT display) for full functionality
- **while-True loops**: Main application has infinite loops that must be stripped for testing
- **OAuth2 token**: Dropbox integration requires manual token setup (TOKEN = 'YOUR_ACCESS_TOKEN' in dropbox_upload.py)
- **INSTALL.sh**: Requires sudo privileges and Raspberry Pi environment

## Notes
- **Key files**: pidslm.py (main GUI application), dropbox_upload.py (Dropbox integration), INSTALL.sh (installation script)
- **Dependencies**: Pillow, guizero, dropbox, guizero[images]
- **Test infrastructure**: tests/conftest.py provides comprehensive hardware mocking for RPi modules
- **Architecture**: Uses guizero App class for GUI, RPi.GPIO for camera control, picamera/picamera2 for camera operations
- **Dropbox integration**: Uses OAuth2 API v2, requires manual token configuration
- **GUI controls**: Provides buttons for photo capture, video recording, and Dropbox upload
