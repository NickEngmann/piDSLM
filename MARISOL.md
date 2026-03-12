# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
Raspberry Pi Digital Single Lens Mirrorless camera interface project with GPIO controls, gallery display, and Dropbox upload functionality. Built with Python 3.12, guizero GUI framework, and RPi.GPIO for hardware interaction.

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
- 2024-01-15: Initial project setup with guizero GUI framework and RPi.GPIO integration
- 2024-01-20: Added Dropbox upload functionality with OAuth2 token configuration
- 2024-02-05: Implemented hardware mocking via conftest.py for test environment
- 2024-02-10: Created test_example.py starter template for hardware simulation tests
- 2024-02-15: Updated requirements.txt with Pillow, guizero, and dropbox dependencies

## Known Issues
- Requires Raspberry Pi hardware for full functionality
- Dropbox OAuth token must be configured in dropbox_upload.py
- GPIO operations need hardware or mocked environment
- Tests currently only include test_example.py template

## Notes
- Main application entry point: pidslm.py
- Test infrastructure: tests/conftest.py with embedded_mocks.py
- Hardware simulation: RPi.GPIO, I2C, SPI, UART mocked via conftest.py
- Dropbox upload: dropbox_upload.py requires valid OAuth token
- Display: MHS35-TFT 3.5 inch display support
- Camera: HQ Camera interface for Raspberry Pi 2/3
- GUI framework: guizero with Picture, Window, PushButton components
- Dependencies: Pillow for image handling, guizero[images] for image support

## Last Result
- **Status**: PASS
- **Tests**: 1 passed, 0 failed
- **Coverage**: Hardware mocks working correctly
- **Date**: 2024-02-15
- **Test file**: tests/test_example.py
- **Mock modules**: RPi.GPIO, guizero, I2C, SPI, UART
