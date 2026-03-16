# MARISOL.md — Pipeline Context for piDSLM

## Project Overview
Raspberry Pi camera interface with GPIO controls, gallery display, and Dropbox upload functionality using guizero GUI.

**Repository**: `NickEngmann/piDSLM`
**Language**: python
**Framework**: guizero
**Subtype**: rpi_python
**Docker Image**: `lotus-rpi-python:latest` — use this for all testing


## Build & Run
- **Install deps**: `cd /workspace/repo && pip install  -r requirements.txt 2>&1 | tail -5 || true; pip install  pytest 2>&1 | tail -3`


## Testing
- **Has existing tests**: yes
- **Test directory**: `tests/`
- **Test framework**: pytest
- **Test command**: `pytest tests/ -v`
- **Pipeline test runner**: `cd /workspace/repo && xvfb-run -a python3 -m pytest tests/ -v --tb=short -p no:debugging 2>&1 || xvfb-run -a python3 -m pytest . -v --tb=short -p no:debugging --ignore=mocks/ 2>&1`
- **Testable components** (partial scope): dropbox_upload.py, tests/embedded_mocks.py, tests/conftest.py

### RPi Python Testing Notes
- ALWAYS use `xvfb-run -a` prefix for pytest (GUI deps need virtual display)
- Use existing conftest.py and mocks if present — DO NOT create new ones
- Hardware modules (RPi.GPIO, etc.) are pre-mocked in the container


## File Structure
**Source files:**
- `pidslm.py`
- `dropbox_upload.py`
**Test files:**
- `tests/test_example.py`
- `tests/embedded_mocks.py`
- `tests/conftest.py`
**Config/Build files (DO NOT MODIFY):**
- `requirements.txt`


## Key Source Code
Snippets from main source files (first 40 lines each):
```

--- pidslm.py ---
#!/usr/bin/python3
from guizero import App, PushButton, Text, Picture, Window
from time import sleep
import time
import glob
import datetime
import sys, os
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library


class piDSLM:
    def __init__(self):
        self.capture_number = self.timestamp()
        self.video_capture_number = self.timestamp()
        self.picture_index = 0
        self.saved_pictures = [] 
        self.shown_picture = "" 
      
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(16, GPIO.FALLING, callback=self.takePicture, bouncetime=2500)
            
        self.app = App(layout="grid", title="Camera Controls", bg="black", width=480, height=320)

        text0 = Text(self.app,color="white", grid=[1,0], text="- PiDSLM -")

        button1 = PushButton(self.app, grid=[1,1], width=110, height=110, pady=35, padx=10, image="/home/pi/piDSLM/icon/prev.png", command=self.long_preview)
        text1 = Text(self.app, color="white", grid=[1,2],text="Focus")

        button2 = PushButton(self.app, grid=[3,1], width=110, height=110, pady=35, padx=10, image="/home/pi/piDSLM/icon/gallery.png", command=self.show_gallery)
        text2 = Text(self.app, color="white", grid=[3,2],text="Gallery")

        button3 = PushButton(self.app, grid=[5,1], width=110, height=110,  pady=35, padx=10, image="/home/pi/piDSLM/icon/vid.png", command=self.video_capture)
        text2 = Text(self.app, color="white", grid=[5,2],text="HD 30s")

        button4 = PushButton(self.app, grid=[7,1], width=110, height=110, pady=35, padx=10, image="/home/pi/piDSLM/icon/lapse.png", command=self.burst)
        text3 = Text(self.app, color="white", grid=[7,2],text="Burst")

        button5 = PushButton(self.app, grid=[1,3], width=110, height=110, image="/home/pi/piDSLM/icon/self.png", command=se
```


## CI Gotchas
(none yet — will be populated if CI fails)


## Pipeline History
- *2026-03-16* — Scout: python/guizero, scope=partial

- *2026-03-16* — Implement: ## Summary

Successfully implemented real features for the piDSLM project by fixing compatibility is

## Known Issues
(none yet)


## Notes
- This file is auto-read by Qwen Code as project context (like CLAUDE.md)
- Updated by each pipeline phase with learnings, CI fixes, and gotchas
- DO NOT delete this file — it helps the pipeline avoid repeating mistakes

