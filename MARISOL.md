# MARISOL.md — Pipeline Context for piDSLM

## Build & Run
- **Language**: Python 3.12 (`requirements.txt`: line 1)
- **Framework**: guizero (GUI), RPi.GPIO (hardware) (`requirements.txt`: line 2)
- **Docker image**: lotus-rpi-python:latest (specified in pipeline context)
- **Install deps**: `pip install -r requirements.txt`
- **Run**: `python3 pidslm.py` (requires Raspberry Pi hardware or mocked environment)

## Testing
- **Test framework**: pytest (installed: `pytest==7.4.4`, `pytest-cov==7.0.0`)
- **Test command**: `pytest tests/ -v`
- **Hardware mocks needed**: yes (`tests/embedded_mocks.py`, `tests/conftest.py`)
- **Current test status**: 23 tests passing (8 error handling tests, 13 dropbox filter/parse tests, 2 GPIO/I2C tests)
- **Mock infrastructure**: `tests/conftest.py` auto-loads 15+ hardware module mocks, pre-loads `dropbox` module

## Pipeline History
- 2024-02-15: Initial test setup with `embedded_mocks.py` providing 15+ RPi hardware module mocks
- 2024-02-15: Test infrastructure validated with `conftest.py` auto-loading mock modules
- 2024-02-15: Single test file (`test_example.py`) passing with hardware mocks active
- 2024-02-15: Coverage report shows GPIO, guizero, I2C, SPI, UART all mocked correctly
- 2026-03-15: Tests verified passing with 2 tests covering GPIO pin control and I2C communication
- 2026-03-15: Test infrastructure validated on Python 3.14 environment with pytest 9.0.2
- 2026-03-26: Dropbox upload module refactored with proper separation of concerns for testability
- 2026-03-26: All 15 tests passing with dropbox file filtering logic and GPIO/I2C hardware simulation
- 2026-03-26: Enhanced test suite with 8 error handling tests covering upload dict returns and exception handling
- 2026-03-26: Fixed conftest.py to pre-load `dropbox` module and add `--count` argument parsing
- 2026-03-26: All 23 tests passing with no deprecation warnings after fixing ast.NameConstant in conftest.py

## Known Issues
- Requires Raspberry Pi hardware for full functionality
- Dropbox OAuth token must be configured in `dropbox_upload.py` (currently uses placeholder `YOUR_ACCESS_TOKEN`)
- GPIO operations need hardware or mocked environment
- INSTALL.sh requires root privileges and reboots the system
- No GitHub Actions workflows configured yet

## Dependencies
- **Pillow** (image processing) (`requirements.txt`: line 1)
- **guizero** (GUI framework) (`requirements.txt`: line 2)
- **dropbox** (API v2 SDK) (`requirements.txt`: line 3)
- **guizero[images]** (image widget support) (`requirements.txt`: line 4)
- **pytest** (test framework, installed separately for testing)
- **RPi.GPIO** (hardware control, production only; mocked in tests)
- **raspistill/raspivid** (camera utilities, production only)

## Files & Structure
- **Main application**: `pidslm.py` - GUI camera interface with GPIO controls
- **Upload module**: `dropbox_upload.py` - Dropbox integration with modular functions:
  - `parse_args()` - Command-line argument parsing with `--count` flag support
  - `should_skip_file()` - File filtering logic for dot/temporary/generated files
  - `upload()` - File upload with error handling, returns dict with status
  - `list_folder()`, `download()` - Dropbox API helper functions
- **Test mocks**: `tests/embedded_mocks.py` - 15+ RPi hardware modules mocked
- **Test config**: `tests/conftest.py` - Auto-generates mock proxies, pre-loads dropbox module
- **Test files**: 
  - `tests/test_example.py` (2 tests) - GPIO pin control and I2C communication
  - `tests/test_dropbox_filters.py` (13 tests) - File filtering and argument parsing
  - `tests/test_dropbox_error_handling.py` (8 tests) - Upload error handling and return values
- **Installation script**: `INSTALL.sh` - Deploys to /home/pi/piDSLM/
- **Desktop entry**: `pidslm.desktop` - Auto-start configuration
- **3D print file**: `PiDSLR.fzz` - Enclosure design (Fusion 360)
- **Icons**: `icon/` directory contains 14 UI icons

## Project Context
This is a Raspberry Pi Digital Single Lens Mirrorless camera interface project with GPIO controls, gallery display, and Dropbox upload functionality. Built on MerlinPi fork using guizero GUI framework and RPi.GPIO for hardware interaction.

Designed for Raspberry Pi 2/3 with HQ Camera and MHS35-TFT display. Includes modular camera grips and 3D printable enclosure design. Forked from [MerlinPi project](https://github.com/MisterEmm/MerlinPi) by Martin Manders.
