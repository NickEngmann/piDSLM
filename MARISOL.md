# MARISOL.md — Pipeline Context

## Project Overview
Raspberry Pi Digital Single Lens Mirrorless camera interface project with GPIO controls, gallery display, and Dropbox upload functionality. Built with Python 3, guizero GUI framework, and RPi.GPIO for hardware control.

## Build & Run
- **Language**: Python 3.12
- **Framework**: guizero (GUI), RPi.GPIO (hardware)
- **Docker image**: python:3.12-slim
- **Install deps**: `pip install -r requirements.txt`
- **Run**: `python3 pidslm.py` (requires Raspberry Pi hardware or mocked environment)

## Testing
- **Test framework**: pytest
- **Test command**: `pytest tests/ -v`
- **Hardware mocks needed**: yes (rpi_python via conftest.py embedded_mocks)
- **Known test issues**: Tests require embedded_mocks.py for GPIO/I2C/SPI/UART simulation

## Pipeline History
- *2026-03-04* — Implement: Improve pidslm.py main application logic
- *2026-03-10* — Implement: Improve test_pidslm.py and embedded_mocks.py
- *2026-03-10* — Test: 16/19 tests passed with hardware mocks

## Known Issues
- Requires Raspberry Pi hardware for full functionality
- Dropbox OAuth token must be configured in dropbox_upload.py
- GPIO operations need hardware or mocked environment

## Notes
- conftest.py auto-generates hardware mocks for 15+ RPi modules
- embedded_mocks.py provides MockGPIO, MockI2C, MockSPI, MockUART
- INSTALL.sh script handles setup on Raspberry Pi
- Main entry point: pidslm.py with guizero GUI
- Gallery displays images from /home/pi/Pictures/ directory
- Dropbox upload requires valid OAuth token
