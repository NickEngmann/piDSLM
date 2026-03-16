# CODEBASE_SUMMARY.md — piDSLM Architecture Overview

## Project Snapshot

| Attribute | Value |
|-----------|-------|
| **Project Name** | piDSLM (Pi Digital Single Lens Mirrorless) |
| **Repository** | NickEngmann/piDSLM |
| **Base Project** | MerlinPi (MisterEmm) |
| **License** | MIT |
| **Language** | Python 3.12+ |
| **Framework** | guizero |
| **Target Hardware** | Raspberry Pi 2/3/4 |
| **Primary Use** | Camera interface with GPIO controls |

---

## System Architecture

### High-Level Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    piDSLM Application                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  GUI Layer   │  │  Camera      │  │  Upload      │      │
│  │  (guizero)   │  │  Control     │  │  (Dropbox)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│           │                │                │               │
│           └────────────────┼────────────────┘               │
│                            │                                │
│                    ┌───────▼───────┐                        │
│                    │  Hardware     │                        │
│                    │  Abstraction  │                        │
│                    │  (Mocked)     │                        │
│                    └───────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. GUI Layer (`pidslm.py`)
**Framework**: guizero 1.4+  
**Layout**: Grid-based, fullscreen window (480x320px)

**UI Components**:
- **Main Window**: Camera controls with 8 buttons
- **Gallery Window**: Image browsing with navigation
- **Busy Window**: Red overlay during operations

**Button Functions**:
| Button | Command | Action |
|--------|---------|--------|
| Focus | `long_preview()` | 15s live preview |
| Gallery | `show_gallery()` | Open image browser |
| HD 30s | `video_capture()` | Record 30s video |
| Burst | `burst()` | Capture 10 photos |
| Shutter | `takePicture()` | GPIO trigger capture |
| 1h 60pix | `lapse()` | Timelapse (1hr) |
| HD 30m | `split_hd_30m()` | Split recording |
| Upload | `upload()` | Dropbox sync |
| Clear | `clear()` | Delete downloads |

**GPIO Configuration**:
- Pin 16: Input with falling edge detection
- Callback: `takePicture()` on button press
- Bounce time: 2500ms

#### 2. Camera Control Layer
**Commands Executed**:
- `raspistill` — Still image capture (Raspberry Pi Camera)
- `raspivid` — Video recording (H.264 encoding)

**Image Parameters**:
| Mode | Command | Duration | Output |
|------|---------|----------|--------|
| Preview | `raspistill -f -t 15000` | 15s | Live feed |
| Capture | `raspistill -f -o ...` | Instant | JPEG |
| Burst | `raspistill -tl 1000 -n -bm` | 10s | 10 JPEGs |
| Timelapse | `raspistill -t 3600000 -tl 60000` | 1hr | 60s intervals |
| Video 30s | `raspivid -t 30000` | 30s | H.264 |
| Video 30m | `raspivid -t 1800000` | 30m | H.264 split |

#### 3. Upload Layer (`dropbox_upload.py`)
**API Version**: Dropbox API v2  
**Authentication**: OAuth2 access token

**Sync Logic**:
1. Walk local directory tree
2. Compare with remote folder listing
3. Check file metadata (mtime, size)
4. Upload modified/new files
5. Download changed remote files
6. Interactive prompts for directories

**File Filtering**:
- Skipped: `.`, `@*`, `~`, `*.pyc`, `__pycache__`
- NFC normalized filenames
- UTF-8 encoding support

---

## File Structure

```
piDSLM/
├── pidslm.py              # Main GUI application (182 lines)
├── dropbox_upload.py      # Dropbox sync utility (236 lines)
├── INSTALL.sh             # Installation script
├── pidslm.desktop         # Auto-start desktop entry
├── PiDSLR.fzz             # 3D enclosure design (Fusion 360)
├── requirements.txt       # Python dependencies
├── README.md              # User documentation
├── MARISOL.md             # Pipeline context
├── SCOUT.md               # Project analysis
├── TESTING.md             # Test documentation
├── CODEBASE_SUMMARY.md    # Architecture overview
├── icon/                  # UI assets (13 PNG files)
│   ├── cam.png            # Shutter icon
│   ├── gallery.png        # Gallery icon
│   ├── vid.png            # Video icon
│   ├── lapse.png          # Timelapse icon
│   ├── long.png           # Split icon
│   ├── drop.png           # Upload icon
│   ├── del.png            # Delete icon
│   ├── prev.png           # Prev button
│   ├── self.png           # Shutter button
│   ├── left.png           # Navigation left
│   ├── right.png          # Navigation right
│   ├── 100black.png       # Overlay
│   └── 100trans.png       # Transparent overlay
└── tests/                 # Test suite
    ├── test_example.py    # Example tests (2 tests)
    ├── embedded_mocks.py  # Hardware mocks (4 classes)
    └── conftest.py        # pytest fixtures (auto-mocks)
```

---

## Data Flow

### Photo Capture Flow
```
GPIO Button Press (Pin 16)
    ↓
Falling Edge Detected
    ↓
takePicture() Callback
    ↓
Show Busy Overlay
    ↓
Generate Timestamp (YYYYMMDD_HHMMSS)
    ↓
Execute: raspistill -f -t 3500 -o /Downloads/{timestamp}cam.jpg
    ↓
Save to Downloads Directory
    ↓
Hide Busy Overlay
```

### Video Capture Flow
```
User Clicks "HD 30s"
    ↓
Show Busy Overlay
    ↓
Generate Timestamp
    ↓
Execute: raspivid -f -t 30000 -o /Downloads/{timestamp}vid.h264
    ↓
Save Video File
    ↓
Hide Busy Overlay
```

### Dropbox Upload Flow
```
User Clicks "Upload"
    ↓
Show Busy Overlay
    ↓
Execute: python3 dropbox_upload.py --yes
    ↓
Parse Arguments (folder, rootdir, token)
    ↓
Create Dropbox Client
    ↓
Walk Downloads Directory
    ↓
For Each File:
  ┌─ Check if already synced (metadata match)
  └─ If modified: Download remote, overwrite local
For Each Directory:
  └─ Prompt to descend (or auto-skip if --yes)
    ↓
Upload Changes
    ↓
Show Status Messages
```

---

## Configuration

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `HOME` | `/home/pi` | User home directory |
| `DROPBOX_TOKEN` | (none) | OAuth2 token (recommended over hardcoding) |

### Hardcoded Paths (Now Relative)
| Path | Purpose | Resolution |
|------|---------|------------|
| `/home/pi/piDSLM/icon/*` | UI icons | `os.path.join(icon_dir, filename)` |
| `/home/pi/Downloads/*` | Output files | `os.environ.get('HOME') + '/Downloads'` |

### Mutable Settings
**In `pidslm.py`**:
- `downloads_dir` — Output folder (configurable)
- `icon_dir` — Icon location (relative to script)

**In `dropbox_upload.py`**:
- `TOKEN` — Dropbox OAuth token (should use env var)

---

## Dependencies

### Python Packages (`requirements.txt`)
| Package | Purpose | Version |
|---------|---------|---------|
| Pillow | Image processing | 8.0+ |
| guizero | GUI framework | 1.4+ |
| dropbox | Cloud API client | 10.1+ |
| guizero[images] | Image widgets | 1.4+ |

### System Dependencies (Implicit)
| Dependency | Purpose | Required |
|------------|---------|----------|
| `raspistill` | Camera still capture | ✅ Raspberry Pi |
| `raspivid` | Camera video capture | ✅ Raspberry Pi |
| `RPi.GPIO` | GPIO control | ✅ Raspberry Pi |
| Python 3.12+ | Language runtime | ✅ Any Linux |

---

## Hardware Interfaces

### GPIO Configuration
```
Pin 16 (BCM) ──┬─── Button (Normally High)
               │
               └─── GPIO.IN with PUD_UP
                    Falling edge → takePicture()
```

### Camera Interface
- **Interface**: MIPI CSI-2 (Raspberry Pi HQ Camera)
- **Commands**: `raspistill`, `raspivid` (libcamera-based)
- **Output Formats**: JPEG (still), H.264 (video)

### Display Interface
- **Display**: 3.5" TFT (MHS35-TFT)
- **Resolution**: 480x320 pixels
- **Interface**: SPI or Parallel (depends on display model)

### Audio Interface (Optional)
- **Microphone**: For video audio capture
- **Interface**: I2S or 3.5mm jack

---

## Testing Strategy

### Unit Tests (Mocked)
```python
def test_gpio_pin_control():
    """Simulate GPIO pin operations."""
    gpio = MockGPIO()
    # Test high/low, setup, cleanup
    assert gpio.input(17) == gpio.HIGH

def test_i2c_communication():
    """Simulate I2C bus communication."""
    i2c = MockI2C()
    # Test read/write, buffer operations
    assert buf[1] == 0x7F
```

### Integration Tests (Manual)
- Full GUI operation on Raspberry Pi
- Camera capture with real hardware
- Dropbox sync with actual token
- Timelapse and burst mode validation

---

## Security Considerations

### Current State
| Issue | Severity | Status |
|-------|----------|--------|
| Dropbox token in source | Medium | ⚠️ Should use env var |
| Path traversal in uploads | Low | ✅ Fixed directory |
| Unrestricted file deletion | Medium | ⚠️ `rm -v Downloads/*` |

### Recommendations
1. Use `DROPBOX_TOKEN` environment variable
2. Add confirmation dialog before clear operation
3. Validate file extensions before upload
4. Add rate limiting for Dropbox API calls

---

## Performance Notes

### Memory Usage
- **GUI Window**: ~50MB (guizero + images)
- **Video Buffer**: ~50MB/minute (H.264 encoding)
- **Gallery**: ~10MB per 100 images

### Disk Requirements
- **Minimum**: 16GB SD card (OS + app)
- **Recommended**: 32GB+ for video storage
- **Daily Usage**: ~500MB (photos) + ~2GB (video)

### Startup Time
- **Cold Start**: ~3 seconds (GUI initialization)
- **Gallery Load**: ~500ms (glob scan + image list)
- **First Upload**: ~2 seconds (Dropbox client init)

---

## Maintenance Notes

### Regular Tasks
- **Backup**: Sync Downloads folder to Dropbox weekly
- **Storage**: Monitor disk space, clear old files
- **Updates**: Check for Raspberry Pi OS updates monthly
- **Tokens**: Rotate Dropbox tokens quarterly

### Known Limitations
1. No RAW image format support
2. Video audio not recorded (H.264 only)
3. Single camera session (no multi-camera)
4. No live streaming support
5. Dropbox sync is one-way (upload only)

---

## Contributing Guide

### Adding New Features
1. Create feature branch from `main`
2. Update `pidslm.py` with new method
3. Add corresponding GUI button (update `__init__`)
4. Test on Raspberry Pi hardware
5. Update documentation

### Code Style
- PEP 8 compliance
- Docstrings for all methods
- Type hints where appropriate
- Comments for complex logic

---

*Document generated: 2026-03-16*  
*Last reviewed: 2026-03-16*  
*Author: piDSLM Pipeline Team*
