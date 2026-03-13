# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
Raspberry Pi Digital Single Lens Mirrorless camera interface project with GPIO controls, gallery display, and Dropbox upload functionality. Built on MerlinPi fork using guizero GUI framework and RPi.GPIO for hardware interaction.

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
- **2024-02-15**: Initial test setup with embedded_mocks.py providing 15+ RPi hardware module mocks
- **2024-02-15**: Test infrastructure validated with conftest.py auto-loading mock modules
- **2024-02-15**: Single test file (test_example.py) passing with hardware mocks active
- **2024-02-15**: Coverage report shows GPIO, guizero, I2C, SPI, UART all mocked correctly

## Known Issues
- Requires Raspberry Pi hardware for full functionality
- Dropbox OAuth token must be configured in dropbox_upload.py
- GPIO operations need hardware or mocked environment
- Tests currently only include test_example.py template
- No GitHub Actions workflows configured yet

## Notes
- **Main application**: pidslm.py - GUI camera interface
- **Upload module**: dropbox_upload.py - Dropbox integration
- **Test mocks**: tests/embedded_mocks.py - 15+ hardware modules mocked
- **Test config**: tests/conftest.py - Auto-generates mock proxies
- **Dependencies**: Pillow, guizero, dropbox, guizero[images]
- **Installation script**: INSTALL.sh - Deploys to /home/pi/piDSLM/
- **Desktop entry**: pidslm.desktop - Auto-start configuration
- **3D print file**: PiDSLR.fzz - Enclosure design
- **Icons**: icon/ directory contains 14 UI icons
- **Hardware**: Designed for Raspberry Pi 2/3 + HQ Camera + MHS35-TFT
- **Base project**: Forked from MerlinPi (MisterEmm)
