# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
Raspberry Pi Digital Single Lens Mirrorless camera interface with GPIO controls, gallery display, and Dropbox upload functionality. Built on MerlinPi fork using guizero GUI framework and RPi.GPIO for hardware interaction.


## Build & Run
- **Language**: Python 3.12
- **Framework**: guizero (GUI), RPi.GPIO (hardware)
- **Dependencies**: Pillow, guizero, dropbox, guizero[images] (from requirements.txt)
- **Test framework**: pytest
- **Test command**: python3 -m pytest tests/ -v
- **Hardware mocks**: embedded_mocks.py provides 15+ RPi hardware module mocks
- **Install deps**: pip install -r requirements.txt
- **Run**: python3 pidslm.py (requires Raspberry Pi hardware or mocked environment)


## Testing
- **Test count**: 2 tests passing (test_gpio_pin_control, test_i2c_communication)
- **Test location**: tests/test_example.py
- **Hardware mocks location**: tests/embedded_mocks.py (MockGPIO, MockI2C, MockSPI, MockUART classes)
- **Test config**: tests/conftest.py (auto-generates mock proxies for RPi modules)
- **Source module fixture**: Auto-strips while-True loops from source files before loading


## Pipeline History
- **2024-02-15**: Initial test setup with embedded_mocks.py providing 15+ RPi hardware module mocks
- **2024-02-15**: Test infrastructure validated with conftest.py auto-loading mock modules
- **2024-02-15**: Single test file (test_example.py) passing with hardware mocks active
- **2024-02-15**: Coverage report shows GPIO, guizero, I2C, SPI, UART all mocked correctly
- **2026-03-15**: Tests verified passing with 2 tests covering GPIO pin control and I2C communication
- **2026-03-15**: Test infrastructure validated on Python 3.14 environment with pytest 9.0.2
- **2026-03-22**: All 21 tests pass (14 for dropbox_upload + 7 for example hardware tests)
- **2026-03-23**: API errors encountered during tool choice configuration
- **2026-03-24**: Continued API configuration issues resolved

- *2026-03-26* — Implement: All 30 tests pass. Let me create a quick summary of what was implemented:

---

## Summary

I'\''ve suc

## Known Issues
- Requires Raspberry Pi hardware for full functionality
- Dropbox OAuth token must be configured in dropbox_upload.py (TOKEN = "YOUR_ACCESS_TOKEN")
- GPIO operations need hardware or mocked environment
- Tests currently only include test_example.py template
- No GitHub Actions workflows configured yet
- Hardcoded paths in pidslm.py (/home/pi/piDSLM/) need configuration


## Notes
- **Main application**: pidslm.py - GUI camera interface (lines 1-134 in pidslm.py)
- **Upload module**: dropbox_upload.py - Dropbox integration (lines 1-158 in dropbox_upload.py)
- **Test mocks**: tests/embedded_mocks.py - 15+ hardware modules mocked
- **Test config**: tests/conftest.py - Auto-generates mock proxies
- **Dependencies**: Pillow, guizero, dropbox, guizero[images] (from requirements.txt lines 1-4)
- **Installation script**: INSTALL.sh - Deploys to /home/pi/piDSLM/
- **Desktop entry**: pidslm.desktop - Auto-start configuration
- **3D print file**: PiDSLR.fzz - Enclosure design
- **Icons**: icon/ directory contains 14 UI icons (cam, gallery, lapse, drop, del, etc.)
- **Hardware**: Designed for Raspberry Pi 2/3 + HQ Camera + MHS35-TFT
- **Base project**: Forked from MerlinPi (MisterEmm) - see README.md Installation section


## Source Attribution
- **requirements.txt**: Lines 1-4 list all Python dependencies
- **README.md**: Lines 1-63 contain user-facing documentation
- **pidslm.py**: Lines 1-134 main application with GPIO setup (line 7) and GUI controls
- **dropbox_upload.py**: Lines 1-158 Dropbox sync functionality with OAuth2 token at line 19
- **INSTALL.sh**: Lines 1-16 installation and auto-start configuration
- **tests/conftest.py**: Lines 1-167 test configuration with auto-mocking
- **tests/embedded_mocks.py**: Lines 1-194 hardware simulation mocks
- **tests/test_example.py**: Lines 1-27 test examples for GPIO and I2C

