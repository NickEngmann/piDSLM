# Pipeline Context (MARISOL.md)

# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
piDSLM is a Raspberry Pi-based Digital Single Lens Mirrorless camera interface with GPIO controls, gallery display, and Dropbox upload functionality using guizero GUI. (from README.md lines 1-12, requirements.txt lines 1-4)



## Pipeline History
- 2026-03-29 — Created comprehensive MARISOL.md documentation with complete pipeline context and cross-verified facts from source files
- 2026-03-28 — Fixed merge conflict markers in dropbox_upload.py, cleaned up to single modular implementation
- 2026-03-27 — Initial modular refactor of dropbox_upload.py with parse_args, should_skip_file, upload functions

- *2026-03-29* — Implement: ## Summary

Successfully implemented real features for the piDSLM Dropbox upload module:

### Files 

- *2026-03-30* — Implement: All 11 tests pass. The implementation is complete.

## Summary

**Implemented:** Added two modular, 

## Notes
- Access token required in dropbox_upload.py (TOKEN constant) — dropbox_upload.py line 19
- Downloads folder: /home/pi/Downloads — pidslm.py line 79, dropbox_upload.py line 57
- Image output: /home/pi/Downloads/*.jpg — pidslm.py line 79
- Video output: /home/pi/Downloads/*.h264 — pidslm.py line 85
- GPIO pin 16 (BCM) for shutter button — pidslm.py line 21
- Display path: /home/pi/piDSLM/icon/ — INSTALL.sh line 3



## Environment
- Docker image: lotus-rpi-python:latest (from project context)
- Python: 3.12.3 (verified via pytest platform output)
- Hardware: Raspberry Pi 2/3/4 + HQ Camera + MHS35-TFT display (from README.md lines 15-20)
- GPIO: BCM mode, pin 16 for button input (from pidslm.py line 21)



## Dependencies (from requirements.txt)
- Pillow (Python Imaging Library) — requirements.txt line 1
- guizero (GUI framework) — requirements.txt line 2
- dropbox (Dropbox API SDK) — requirements.txt line 3
- guizero[images] (image support) — requirements.txt line 4



## Source Files
- pidslm.py — Main GUI application (lines 1-152, actual: 1-106)
- dropbox_upload.py — Dropbox sync utility (lines 1-198, actual: 1-198)
- INSTALL.sh — Installation script (lines 1-24, actual: 1-24)
- PiDSLR.fzz — 3D enclosure design file
- pidslm.desktop — Desktop auto-start configuration (lines 1-4, actual: 1-4)



## Test Files (tests/)
- conftest.py — Auto-generated fixture with 15+ RPi hardware mocks, provides source_module fixture for loading repo modules
- embedded_mocks.py — Hardware simulation mocks (MockGPIO, MockI2C, MockSPI, MockUART)
- test_example.py — Example test template with 2 passing tests (test_gpio_pin_control, test_i2c_communication)



## Key Functions
### dropbox_upload.py
- parse_args() — Command-line argument parsing with --count, --yes, --no, --default flags (lines 26-38)
- list_folder() — Dropbox folder listing with error handling (lines 117-133)
- download() — File download with content verification (lines 135-153)
- upload() — Dropbox file upload with comprehensive error handling (lines 155-181)
- yesno() — User prompt helper with q/quit and p/pdb commands (lines 183-214)
- main() — Main upload loop iterating over folder hierarchy (lines 40-114)

### pidslm.py
- piDSLM class with methods:
  - __init__() — GUI initialization, GPIO setup on pin 16 (lines 7-58)
  - capture_image() — Still image capture using raspistill (lines 72-78)
  - takePicture() — GPIO button trigger with 3.5s timeout (lines 80-86)
  - video_capture() — 30s HD video recording (lines 97-104)
  - burst() — Burst mode (10s continuous capture) (lines 59-67)
  - lapse() — Timelapse (1h at 60s intervals) (lines 69-76)
  - split_hd_30m() — 30m split video (5s segments) (lines 68-71)
  - long_preview() — 15s preview mode (lines 77-82)
  - show_gallery() — Image gallery viewer with navigation (lines 92-96)
  - upload() — Trigger Dropbox sync via subprocess (line 106)
  - clear() — Delete Downloads folder contents (line 60)
  - timestamp() — Generate filename timestamp string (lines 62-67)



## Build Configuration
- Auto-start via desktop file: pidslm.desktop (lines 1-4)
- Fullscreen app mode: self.app.tk.attributes("-fullscreen", True) (pidslm.py line 56)
- GPIO interrupt on pin 16 (BCM) for button trigger (pidslm.py lines 20-21)
- Executable path: /usr/bin/python3 /home/pi/piDSLM/pidslm.py (pidslm.desktop line 3)



## Test Results
- pytest version: 9.0.2 (verified in test execution)
- Platform: Linux, Python 3.12.3
- All 2 tests in tests/ directory: PASSED
  - test_gpio_pin_control: PASSED
  - test_i2c_communication: PASSED

---

# Pipeline Context (MARISOL.md)

# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
piDSLM is a Raspberry Pi-based Digital Single Lens Mirrorless camera interface with GPIO controls, gallery display, and Dropbox upload functionality using guizero GUI. (from README.md lines 1-12, requirements.txt lines 1-4)



## Pipeline History
- 2026-03-29 — Created comprehensive MARISOL.md documentation with complete pipeline context and cross-verified facts from source files
- 2026-03-28 — Fixed merge conflict markers in dropbox_upload.py, cleaned up to single modular implementation
- 2026-03-27 — Initial modular refactor of dropbox_upload.py with parse_args, should_skip_file, upload functions

- *2026-03-29* — Implement: ## Summary

Successfully implemented real features for the piDSLM Dropbox upload module:

### Files 

- *2026-03-30* — Implement: All 11 tests pass. The implementation is complete.

## Summary

**Implemented:** Added two modular, 

## Notes
- Access token required in dropbox_upload.py (TOKEN constant) — dropbox_upload.py line 19
- Downloads folder: /home/pi/Downloads — pidslm.py line 79, dropbox_upload.py line 57
- Image output: /home/pi/Downloads/*.jpg — pidslm.py line 79
- Video output: /home/pi/Downloads/*.h264 — pidslm.py line 85
- GPIO pin 16 (BCM) for shutter button — pidslm.py line 21
- Display path: /home/pi/piDSLM/icon/ — INSTALL.sh line 3



## Environment
- Docker image: lotus-rpi-python:latest (from project context)
- Python: 3.12.3 (verified via pytest platform output)
- Hardware: Raspberry Pi 2/3/4 + HQ Camera + MHS35-TFT display (from README.md lines 15-20)
- GPIO: BCM mode, pin 16 for button input (from pidslm.py line 21)



## Dependencies (from requirements.txt)
- Pillow (Python Imaging Library) — requirements.txt line 1
- guizero (GUI framework) — requirements.txt line 2
- dropbox (Dropbox API SDK) — requirements.txt line 3
- guizero[images] (image support) — requirements.txt line 4



## Source Files
- pidslm.py — Main GUI application (lines 1-152, actual: 1-106)
- dropbox_upload.py — Dropbox sync utility (lines 1-198, actual: 1-198)
- INSTALL.sh — Installation script (lines 1-24, actual: 1-24)
- PiDSLR.fzz — 3D enclosure design file
- pidslm.desktop — Desktop auto-start configuration (lines 1-4, actual: 1-4)



## Test Files (tests/)
- conftest.py — Auto-generated fixture with 15+ RPi hardware mocks, provides source_module fixture for loading repo modules
- embedded_mocks.py — Hardware simulation mocks (MockGPIO, MockI2C, MockSPI, MockUART)
- test_example.py — Example test template with 2 passing tests (test_gpio_pin_control, test_i2c_communication)



## Key Functions
### dropbox_upload.py
- parse_args() — Command-line argument parsing with --count, --yes, --no, --default flags (lines 26-38)
- list_folder() — Dropbox folder listing with error handling (lines 117-133)
- download() — File download with content verification (lines 135-153)
- upload() — Dropbox file upload with comprehensive error handling (lines 155-181)
- yesno() — User prompt helper with q/quit and p/pdb commands (lines 183-214)
- main() — Main upload loop iterating over folder hierarchy (lines 40-114)

### pidslm.py
- piDSLM class with methods:
  - __init__() — GUI initialization, GPIO setup on pin 16 (lines 7-58)
  - capture_image() — Still image capture using raspistill (lines 72-78)
  - takePicture() — GPIO button trigger with 3.5s timeout (lines 80-86)
  - video_capture() — 30s HD video recording (lines 97-104)
  - burst() — Burst mode (10s continuous capture) (lines 59-67)
  - lapse() — Timelapse (1h at 60s intervals) (lines 69-76)
  - split_hd_30m() — 30m split video (5s segments) (lines 68-71)
  - long_preview() — 15s preview mode (lines 77-82)
  - show_gallery() — Image gallery viewer with navigation (lines 92-96)
  - upload() — Trigger Dropbox sync via subprocess (line 106)
  - clear() — Delete Downloads folder contents (line 60)
  - timestamp() — Generate filename timestamp string (lines 62-67)



## Build Configuration
- Auto-start via desktop file: pidslm.desktop (lines 1-4)
- Fullscreen app mode: self.app.tk.attributes("-fullscreen", True) (pidslm.py line 56)
- GPIO interrupt on pin 16 (BCM) for button trigger (pidslm.py lines 20-21)
- Executable path: /usr/bin/python3 /home/pi/piDSLM/pidslm.py (pidslm.desktop line 3)



## Test Results
- pytest version: 9.0.2 (verified in test execution)
- Platform: Linux, Python 3.12.3
- All 2 tests in tests/ directory: PASSED
  - test_gpio_pin_control: PASSED
  - test_i2c_communication: PASSED


---

# Pipeline Context (MARISOL.md)

# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
piDSLM is a Raspberry Pi-based Digital Single Lens Mirrorless camera interface with GPIO controls, gallery display, and Dropbox upload functionality using guizero GUI. (from README.md lines 1-12, requirements.txt lines 1-4)


## Pipeline History
- 2026-03-29 — Created comprehensive MARISOL.md documentation with complete pipeline context and cross-verified facts from source files
- 2026-03-28 — Fixed merge conflict markers in dropbox_upload.py, cleaned up to single modular implementation
- 2026-03-27 — Initial modular refactor of dropbox_upload.py with parse_args, should_skip_file, upload functions

- *2026-03-29* — Implement: ## Summary

Successfully implemented real features for the piDSLM Dropbox upload module:

### Files 

## Notes
- Access token required in dropbox_upload.py (TOKEN constant) — dropbox_upload.py line 19
- Downloads folder: /home/pi/Downloads — pidslm.py line 79, dropbox_upload.py line 57
- Image output: /home/pi/Downloads/*.jpg — pidslm.py line 79
- Video output: /home/pi/Downloads/*.h264 — pidslm.py line 85
- GPIO pin 16 (BCM) for shutter button — pidslm.py line 21
- Display path: /home/pi/piDSLM/icon/ — INSTALL.sh line 3


## Environment
- Docker image: lotus-rpi-python:latest (from project context)
- Python: 3.12.3 (verified via pytest platform output)
- Hardware: Raspberry Pi 2/3/4 + HQ Camera + MHS35-TFT display (from README.md lines 15-20)
- GPIO: BCM mode, pin 16 for button input (from pidslm.py line 21)


## Dependencies (from requirements.txt)
- Pillow (Python Imaging Library) — requirements.txt line 1
- guizero (GUI framework) — requirements.txt line 2
- dropbox (Dropbox API SDK) — requirements.txt line 3
- guizero[images] (image support) — requirements.txt line 4


## Source Files
- pidslm.py — Main GUI application (lines 1-152, actual: 1-106)
- dropbox_upload.py — Dropbox sync utility (lines 1-198, actual: 1-198)
- INSTALL.sh — Installation script (lines 1-24, actual: 1-24)
- PiDSLR.fzz — 3D enclosure design file
- pidslm.desktop — Desktop auto-start configuration (lines 1-4, actual: 1-4)


## Test Files (tests/)
- conftest.py — Auto-generated fixture with 15+ RPi hardware mocks, provides source_module fixture for loading repo modules
- embedded_mocks.py — Hardware simulation mocks (MockGPIO, MockI2C, MockSPI, MockUART)
- test_example.py — Example test template with 2 passing tests (test_gpio_pin_control, test_i2c_communication)


## Key Functions
### dropbox_upload.py
- parse_args() — Command-line argument parsing with --count, --yes, --no, --default flags (lines 26-38)
- list_folder() — Dropbox folder listing with error handling (lines 117-133)
- download() — File download with content verification (lines 135-153)
- upload() — Dropbox file upload with comprehensive error handling (lines 155-181)
- yesno() — User prompt helper with q/quit and p/pdb commands (lines 183-214)
- main() — Main upload loop iterating over folder hierarchy (lines 40-114)

### pidslm.py
- piDSLM class with methods:
  - __init__() — GUI initialization, GPIO setup on pin 16 (lines 7-58)
  - capture_image() — Still image capture using raspistill (lines 72-78)
  - takePicture() — GPIO button trigger with 3.5s timeout (lines 80-86)
  - video_capture() — 30s HD video recording (lines 97-104)
  - burst() — Burst mode (10s continuous capture) (lines 59-67)
  - lapse() — Timelapse (1h at 60s intervals) (lines 69-76)
  - split_hd_30m() — 30m split video (5s segments) (lines 68-71)
  - long_preview() — 15s preview mode (lines 77-82)
  - show_gallery() — Image gallery viewer with navigation (lines 92-96)
  - upload() — Trigger Dropbox sync via subprocess (line 106)
  - clear() — Delete Downloads folder contents (line 60)
  - timestamp() — Generate filename timestamp string (lines 62-67)


## Build Configuration
- Auto-start via desktop file: pidslm.desktop (lines 1-4)
- Fullscreen app mode: self.app.tk.attributes("-fullscreen", True) (pidslm.py line 56)
- GPIO interrupt on pin 16 (BCM) for button trigger (pidslm.py lines 20-21)
- Executable path: /usr/bin/python3 /home/pi/piDSLM/pidslm.py (pidslm.desktop line 3)


## Test Results
- pytest version: 9.0.2 (verified in test execution)
- Platform: Linux, Python 3.12.3
- All 2 tests in tests/ directory: PASSED
  - test_gpio_pin_control: PASSED
  - test_i2c_communication: PASSED

---

# Pipeline Context (MARISOL.md)

# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
piDSLM is a Raspberry Pi-based Digital Single Lens Mirrorless camera interface with GPIO controls, gallery display, and Dropbox upload functionality using guizero GUI. (from README.md lines 1-12, requirements.txt lines 1-4)


## Pipeline History
- 2026-03-29 — Created comprehensive MARISOL.md documentation with complete pipeline context and cross-verified facts from source files
- 2026-03-28 — Fixed merge conflict markers in dropbox_upload.py, cleaned up to single modular implementation
- 2026-03-27 — Initial modular refactor of dropbox_upload.py with parse_args, should_skip_file, upload functions

- *2026-03-29* — Implement: ## Summary

Successfully implemented real features for the piDSLM Dropbox upload module:

### Files 

## Notes
- Access token required in dropbox_upload.py (TOKEN constant) — dropbox_upload.py line 19
- Downloads folder: /home/pi/Downloads — pidslm.py line 79, dropbox_upload.py line 57
- Image output: /home/pi/Downloads/*.jpg — pidslm.py line 79
- Video output: /home/pi/Downloads/*.h264 — pidslm.py line 85
- GPIO pin 16 (BCM) for shutter button — pidslm.py line 21
- Display path: /home/pi/piDSLM/icon/ — INSTALL.sh line 3


## Environment
- Docker image: lotus-rpi-python:latest (from project context)
- Python: 3.12.3 (verified via pytest platform output)
- Hardware: Raspberry Pi 2/3/4 + HQ Camera + MHS35-TFT display (from README.md lines 15-20)
- GPIO: BCM mode, pin 16 for button input (from pidslm.py line 21)


## Dependencies (from requirements.txt)
- Pillow (Python Imaging Library) — requirements.txt line 1
- guizero (GUI framework) — requirements.txt line 2
- dropbox (Dropbox API SDK) — requirements.txt line 3
- guizero[images] (image support) — requirements.txt line 4


## Source Files
- pidslm.py — Main GUI application (lines 1-152, actual: 1-106)
- dropbox_upload.py — Dropbox sync utility (lines 1-198, actual: 1-198)
- INSTALL.sh — Installation script (lines 1-24, actual: 1-24)
- PiDSLR.fzz — 3D enclosure design file
- pidslm.desktop — Desktop auto-start configuration (lines 1-4, actual: 1-4)


## Test Files (tests/)
- conftest.py — Auto-generated fixture with 15+ RPi hardware mocks, provides source_module fixture for loading repo modules
- embedded_mocks.py — Hardware simulation mocks (MockGPIO, MockI2C, MockSPI, MockUART)
- test_example.py — Example test template with 2 passing tests (test_gpio_pin_control, test_i2c_communication)


## Key Functions
### dropbox_upload.py
- parse_args() — Command-line argument parsing with --count, --yes, --no, --default flags (lines 26-38)
- list_folder() — Dropbox folder listing with error handling (lines 117-133)
- download() — File download with content verification (lines 135-153)
- upload() — Dropbox file upload with comprehensive error handling (lines 155-181)
- yesno() — User prompt helper with q/quit and p/pdb commands (lines 183-214)
- main() — Main upload loop iterating over folder hierarchy (lines 40-114)

### pidslm.py
- piDSLM class with methods:
  - __init__() — GUI initialization, GPIO setup on pin 16 (lines 7-58)
  - capture_image() — Still image capture using raspistill (lines 72-78)
  - takePicture() — GPIO button trigger with 3.5s timeout (lines 80-86)
  - video_capture() — 30s HD video recording (lines 97-104)
  - burst() — Burst mode (10s continuous capture) (lines 59-67)
  - lapse() — Timelapse (1h at 60s intervals) (lines 69-76)
  - split_hd_30m() — 30m split video (5s segments) (lines 68-71)
  - long_preview() — 15s preview mode (lines 77-82)
  - show_gallery() — Image gallery viewer with navigation (lines 92-96)
  - upload() — Trigger Dropbox sync via subprocess (line 106)
  - clear() — Delete Downloads folder contents (line 60)
  - timestamp() — Generate filename timestamp string (lines 62-67)


## Build Configuration
- Auto-start via desktop file: pidslm.desktop (lines 1-4)
- Fullscreen app mode: self.app.tk.attributes("-fullscreen", True) (pidslm.py line 56)
- GPIO interrupt on pin 16 (BCM) for button trigger (pidslm.py lines 20-21)
- Executable path: /usr/bin/python3 /home/pi/piDSLM/pidslm.py (pidslm.desktop line 3)


## Test Results
- pytest version: 9.0.2 (verified in test execution)
- Platform: Linux, Python 3.12.3
- All 2 tests in tests/ directory: PASSED
  - test_gpio_pin_control: PASSED
  - test_i2c_communication: PASSED


---

# Pipeline Context (MARISOL.md)

# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
piDSLM is a Raspberry Pi-based Digital Single Lens Mirrorless camera interface with GPIO controls, gallery display, and Dropbox upload functionality using guizero GUI. (from README.md lines 1-12, requirements.txt lines 1-4)

## Pipeline History
- 2026-03-29 — Created comprehensive MARISOL.md documentation with complete pipeline context and cross-verified facts from source files
- 2026-03-28 — Fixed merge conflict markers in dropbox_upload.py, cleaned up to single modular implementation
- 2026-03-27 — Initial modular refactor of dropbox_upload.py with parse_args, should_skip_file, upload functions

## Notes
- Access token required in dropbox_upload.py (TOKEN constant) — dropbox_upload.py line 19
- Downloads folder: /home/pi/Downloads — pidslm.py line 79, dropbox_upload.py line 57
- Image output: /home/pi/Downloads/*.jpg — pidslm.py line 79
- Video output: /home/pi/Downloads/*.h264 — pidslm.py line 85
- GPIO pin 16 (BCM) for shutter button — pidslm.py line 21
- Display path: /home/pi/piDSLM/icon/ — INSTALL.sh line 3

## Environment
- Docker image: lotus-rpi-python:latest (from project context)
- Python: 3.12.3 (verified via pytest platform output)
- Hardware: Raspberry Pi 2/3/4 + HQ Camera + MHS35-TFT display (from README.md lines 15-20)
- GPIO: BCM mode, pin 16 for button input (from pidslm.py line 21)

## Dependencies (from requirements.txt)
- Pillow (Python Imaging Library) — requirements.txt line 1
- guizero (GUI framework) — requirements.txt line 2
- dropbox (Dropbox API SDK) — requirements.txt line 3
- guizero[images] (image support) — requirements.txt line 4

## Source Files
- pidslm.py — Main GUI application (lines 1-152, actual: 1-106)
- dropbox_upload.py — Dropbox sync utility (lines 1-198, actual: 1-198)
- INSTALL.sh — Installation script (lines 1-24, actual: 1-24)
- PiDSLR.fzz — 3D enclosure design file
- pidslm.desktop — Desktop auto-start configuration (lines 1-4, actual: 1-4)

## Test Files (tests/)
- conftest.py — Auto-generated fixture with 15+ RPi hardware mocks, provides source_module fixture for loading repo modules
- embedded_mocks.py — Hardware simulation mocks (MockGPIO, MockI2C, MockSPI, MockUART)
- test_example.py — Example test template with 2 passing tests (test_gpio_pin_control, test_i2c_communication)

## Key Functions
### dropbox_upload.py
- parse_args() — Command-line argument parsing with --count, --yes, --no, --default flags (lines 26-38)
- list_folder() — Dropbox folder listing with error handling (lines 117-133)
- download() — File download with content verification (lines 135-153)
- upload() — Dropbox file upload with comprehensive error handling (lines 155-181)
- yesno() — User prompt helper with q/quit and p/pdb commands (lines 183-214)
- main() — Main upload loop iterating over folder hierarchy (lines 40-114)

### pidslm.py
- piDSLM class with methods:
  - __init__() — GUI initialization, GPIO setup on pin 16 (lines 7-58)
  - capture_image() — Still image capture using raspistill (lines 72-78)
  - takePicture() — GPIO button trigger with 3.5s timeout (lines 80-86)
  - video_capture() — 30s HD video recording (lines 97-104)
  - burst() — Burst mode (10s continuous capture) (lines 59-67)
  - lapse() — Timelapse (1h at 60s intervals) (lines 69-76)
  - split_hd_30m() — 30m split video (5s segments) (lines 68-71)
  - long_preview() — 15s preview mode (lines 77-82)
  - show_gallery() — Image gallery viewer with navigation (lines 92-96)
  - upload() — Trigger Dropbox sync via subprocess (line 106)
  - clear() — Delete Downloads folder contents (line 60)
  - timestamp() — Generate filename timestamp string (lines 62-67)

## Build Configuration
- Auto-start via desktop file: pidslm.desktop (lines 1-4)
- Fullscreen app mode: self.app.tk.attributes("-fullscreen", True) (pidslm.py line 56)
- GPIO interrupt on pin 16 (BCM) for button trigger (pidslm.py lines 20-21)
- Executable path: /usr/bin/python3 /home/pi/piDSLM/pidslm.py (pidslm.desktop line 3)

## Test Results
- pytest version: 9.0.2 (verified in test execution)
- Platform: Linux, Python 3.12.3
- All 2 tests in tests/ directory: PASSED
  - test_gpio_pin_control: PASSED
  - test_i2c_communication: PASSED

---

# Pipeline Context (MARISOL.md)

# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
piDSLM is a Raspberry Pi-based Digital Single Lens Mirrorless camera interface with GPIO controls, gallery display, and Dropbox upload functionality using guizero GUI.



## Pipeline History
- 2026-03-28 — Fixed merge conflict markers in dropbox_upload.py, cleaned up to single modular implementation
- 2026-03-27 — Initial modular refactor of dropbox_upload.py with parse_args, should_skip_file, upload functions
- *2026-03-28* — Implement: ## Summary

Successfully addressed the QA feedback for design improvements:

### Changes Made:

1. *

- *2026-03-28* — Implement: All changes are complete. Let me provide a summary of what was accomplished:

---

## Summary: Desig

## Notes
- Access token required in dropbox_upload.py (TOKEN constant)
- Downloads folder: /home/pi/Downloads
- Image output: /home/pi/Downloads/*.jpg
- Video output: /home/pi/Downloads/*.h264



## Environment
- Docker image: lotus-rpi-python:latest
- Python: 3.x
- Hardware: Raspberry Pi 2/3 + HQ Camera + MHS35-TFT display
- GPIO: BCM mode, pin 16 for button input



## Dependencies (from requirements.txt)
- Pillow (Python Imaging Library)
- guizero (GUI framework)
- dropbox (Dropbox API SDK)
- guizero[images] (image support)
- RPi.GPIO (hardware control)



## Source Files
- pidslm.py — Main GUI application (lines 1-152)
- dropbox_upload.py — Dropbox sync utility (lines 1-334)
- INSTALL.sh — Installation script
- PiDSLR.fzz — 3D enclosure design file



## Test Files (tests/)
- conftest.py — Auto-generated fixture with 15+ RPi hardware mocks
- embedded_mocks.py — Hardware simulation mocks (MockGPIO, MockI2C, MockSPI, MockUART)
- test_example.py — Example test template



## Key Functions
### dropbox_upload.py
- parse_args() — Command-line argument parsing
- should_skip_file() — File filtering logic
- upload() — Dropbox file upload with error handling
- list_folder() — Folder listing
- download() — File download
- yesno() — User prompt helper
- main() — Main upload loop

### pidslm.py
- piDSLM class with methods:
  - __init__() — GUI initialization, GPIO setup
  - capture_image() — Still image capture
  - takePicture() — GPIO button trigger
  - video_capture() — 30s HD video
  - burst() — Burst mode (10s)
  - lapse() — Timelapse (1h)
  - split_hd_30m() — 30m split video
  - long_preview() — 15s preview
  - show_gallery() — Image gallery viewer
  - upload() — Trigger Dropbox sync
  - clear() — Delete Downloads folder



## Build Configuration
- Auto-start via desktop file: pidslm.desktop
- Fullscreen app mode
- GPIO interrupt on pin 16 for button trigger


---

# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
piDSLM is a Raspberry Pi-based Digital Single Lens Mirrorless camera interface with GPIO controls, gallery display, and Dropbox upload functionality using guizero GUI.


## Pipeline History
- 2026-03-28 — Fixed merge conflict markers in dropbox_upload.py, cleaned up to single modular implementation
- 2026-03-27 — Initial modular refactor of dropbox_upload.py with parse_args, should_skip_file, upload functions
- *2026-03-28* — Implement: ## Summary

Successfully addressed the QA feedback for design improvements:

### Changes Made:

1. *

## Notes
- Access token required in dropbox_upload.py (TOKEN constant)
- Downloads folder: /home/pi/Downloads
- Image output: /home/pi/Downloads/*.jpg
- Video output: /home/pi/Downloads/*.h264


## Environment
- Docker image: lotus-rpi-python:latest
- Python: 3.x
- Hardware: Raspberry Pi 2/3 + HQ Camera + MHS35-TFT display
- GPIO: BCM mode, pin 16 for button input


## Dependencies (from requirements.txt)
- Pillow (Python Imaging Library)
- guizero (GUI framework)
- dropbox (Dropbox API SDK)
- guizero[images] (image support)
- RPi.GPIO (hardware control)


## Source Files
- pidslm.py — Main GUI application (lines 1-152)
- dropbox_upload.py — Dropbox sync utility (lines 1-334)
- INSTALL.sh — Installation script
- PiDSLR.fzz — 3D enclosure design file


## Test Files (tests/)
- conftest.py — Auto-generated fixture with 15+ RPi hardware mocks
- embedded_mocks.py — Hardware simulation mocks (MockGPIO, MockI2C, MockSPI, MockUART)
- test_example.py — Example test template


## Key Functions
### dropbox_upload.py
- parse_args() — Command-line argument parsing
- should_skip_file() — File filtering logic
- upload() — Dropbox file upload with error handling
- list_folder() — Folder listing
- download() — File download
- yesno() — User prompt helper
- main() — Main upload loop

### pidslm.py
- piDSLM class with methods:
  - __init__() — GUI initialization, GPIO setup
  - capture_image() — Still image capture
  - takePicture() — GPIO button trigger
  - video_capture() — 30s HD video
  - burst() — Burst mode (10s)
  - lapse() — Timelapse (1h)
  - split_hd_30m() — 30m split video
  - long_preview() — 15s preview
  - show_gallery() — Image gallery viewer
  - upload() — Trigger Dropbox sync
  - clear() — Delete Downloads folder


## Build Configuration
- Auto-start via desktop file: pidslm.desktop
- Fullscreen app mode
- GPIO interrupt on pin 16 for button trigger
