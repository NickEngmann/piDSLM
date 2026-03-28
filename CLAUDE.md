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


