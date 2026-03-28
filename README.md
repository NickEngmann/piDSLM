piDSLM - Raspberry Pi Digital Single Lens Mirrorless
===============

Camera project for Raspberry Pi 2/3 + HQ Camera + MHS35-TFT

<img src="https://i.imgur.com/VspFA5V.jpg" data-canonical-src="https://i.imgur.com/VspFA5V.jpg" width="400" height="400" />

# Introduction

Made an enclosure to host the [HQ Raspberry Pi Camera](https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/) as a standalone battery-powered DSLM that I'm calling piDSLM. Check out the links below for instructions on how to recreate the project!

The design includes a few modular camera grips for users. Feel free to make your own designs and reach out to me so I can include them!

For More Info:

- [Hackster](https://www.hackster.io/projects/2a86c3)
- [GitHub](https://github.com/NickEngmann/piDSLM)
- [Instructables] (TBD)

Designed using
- [OnShape](https://bit.ly/raspi-onshape)

If you found this useful, please donate what you think it is worth to my [paypal.me](https://paypal.me/nickengman). Help cover the time of design.

Thanks, Enjoy!

# Installation

For the codebase, I built the piDSLM codebase off of a forked a copy of fellow DIYer Martin Manders [MerlinPi project](https://github.com/MisterEmm/MerlinPi). The piDSLM codebase is still in its infancy but it allows the user to take photos/videos, and view them in a gallery. It also allows users to bulk upload the footage to Dropbox. To begin ssh into the Raspberry Pi and run the following command:

```
git clone https://github.com/NickEngmann/pidslm.git
cd pidslm
```

You're then going to retrieve a Dropbox Access token to enable the Dropbox footage upload feature. To do this go ahead and [go to the Application Developer page on Dropbox](https://www.dropbox.com/developers/apps). Create an application and click the Generate Access Token button to generate your access token.

Then replace the dummy access token in `dropbox_upload.py` with your new access token:

```python
# OAuth2 access token. TODO: login etc.
TOKEN = 'YOUR_ACCESS_TOKEN'
```

Finally, run the INSTALL.sh script using the following command:

```
sudo ./INSTALL.sh
```

# Features

## Capture Modes

### Still Photo Capture
- **Single Photo**: Press button or click "Focus" button for 15-second preview
- **GPIO Button Trigger**: Physical button on GPIO pin 16 triggers instant capture
- **Output Format**: JPEG images saved to `/home/pi/Downloads/`
- **Naming**: Files named with timestamp (e.g., `20260328_143022cam.jpg`)

### Video Recording
- **HD 30s**: Quick video capture at high definition
- **30-minute Split**: Records up to 30 minutes in 5-second segments
- **Output Format**: H.264 video files

### Burst Mode
- Captures up to 10,000 frames over 10 seconds
- Output: `BR<timestamp>%04d.jpg` (numbered sequence)

### Timelapse
- **1-hour Mode**: Captures 60 photos at 1-minute intervals
- **Output**: `TL<timestamp>%04d.jpg` (numbered sequence)

## Gallery Display
- Browse all captured JPEG images in fullscreen
- Navigate using left/right arrow buttons
- Image thumbnails from `/home/pi/Downloads/`

## Dropbox Upload
- Sync captured photos and videos to Dropbox
- Smart upload with duplicate detection
- Automatic folder creation for subdirectories
- **Filtering**: Skips dot files, temporary files, and generated files
- **Count Limit**: Use `--count N` to limit uploads

# Hardware Requirements

- Raspberry Pi 2 or 3
- Raspberry Pi HQ Camera
- MHS35-TFT display (3.5 inch LCD)
- GPIO button connected to pin 16 (BCM numbering)
- Power supply and storage

# Software Requirements

- Raspberry Pi OS (deprecated Raspbian)
- Python 3.x
- Required packages (see `requirements.txt`):
  - `Pillow` — Image processing
  - `guizero` — GUI framework
  - `dropbox` — Dropbox API SDK
  - `RPi.GPIO` — GPIO control

# Usage

## Starting the Application

The application can be started in two ways:

1. **Auto-start on boot**: After installation, the app starts automatically
2. **Manual launch**: Run `python3 pidslm.py` from terminal

## Control Buttons

| Button | Function | Description |
|--------|----------|-------------|
| Focus | Preview | 15-second live preview before capture |
| Gallery | View | Browse all captured images |
| HD 30s | Video | Record 30-second HD video |
| Burst | Burst | Take up to 10,000 photos in 10 seconds |
| 1h 60pix | Timelapse | Hour-long timelapse (1 photo/min) |
| HD 30m in 5s | Split Video | 30-minute video in 5-second segments |
| Upload | Dropbox | Sync files to Dropbox cloud |
| Clear Folder | Delete | Remove all files from Downloads folder |

## Dropbox Command-Line Options

```
python3 dropbox_upload.py [folder] [rootdir] [options]

Arguments:
  folder          Dropbox folder name (default: Downloads)
  rootdir         Local directory to upload (default: ~/Downloads)

Options:
  --token TOKEN   Dropbox API access token
  --yes, -y       Auto-answer yes to all prompts
  --no, -n        Auto-answer no to all prompts
  --default, -d   Use default answers for all prompts
  --count N       Maximum number of files to upload
```

# File Structure

```
piDSLM/
├── pidslm.py              # Main GUI application
├── dropbox_upload.py      # Dropbox sync utility
├── INSTALL.sh             # Installation script
├── PiDSLR.fzz             # 3D enclosure design
├── pidslm.desktop         # Auto-start desktop entry
├── requirements.txt       # Python dependencies
├── icon/                  # GUI icon files
│   ├── 100black.png
│   ├── 100trans.png
│   ├── cam.png
│   ├── del.png
│   ├── drop.png
│   ├── gallery.png
│   ├── lapse.png
│   ├── long.png
│   ├── left.png
│   ├── right.png
│   ├── self.png
│   └── vid.png
└── tests/                 # Unit tests
    ├── conftest.py       # Test fixtures with hardware mocks
    ├── embedded_mocks.py # GPIO/I2C/SPI/UART mocks
    └── test_example.py   # Example tests
```

# Testing

Run the test suite with pytest:

```bash
cd tests
pytest -v
```

The test framework includes mocks for:
- RPi.GPIO (GPIO pin control)
- I2C, SPI, UART hardware interfaces
- guizero GUI components

# Development

## Adding New Features

1. Edit `pidslm.py` for GUI functionality
2. Edit `dropbox_upload.py` for Dropbox sync features
3. Add tests in `tests/` directory
4. Run `pytest` to verify changes

## Custom GPIO Setup

To modify button triggers, edit the GPIO setup in `__init__()`:

```python
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(16, GPIO.FALLING, callback=self.takePicture, bouncetime=2500)
```

Change pin 16 to your desired GPIO number.

# Troubleshooting

## Dropbox Upload Fails
- Check that TOKEN is set correctly in `dropbox_upload.py`
- Verify Dropbox API access token permissions
- Ensure network connection is active

## GPIO Button Not Working
- Check pin wiring (use GPIO numbering, not physical)
- Verify pin 16 is not used by other peripherals
- Test with `gpioread` command

## Display Issues
- Check `start_x=1` and `gpu_mem=128` in `/boot/config.txt`
- Verify MHS35-TFT driver is installed
- Check display connections

## Gallery Doesn't Load Images
- Ensure images are in `/home/pi/Downloads/`
- Verify file permissions
- Check that images are valid JPEG format

# License

This project is built upon the [MerlinPi project](https://github.com/MisterEmm/MerlinPi). The piDSLM modifications and enhancements are provided as-is for educational and hobbyist use.

# Credits

- **Original Concept**: MerlinPi community project
- **piDSLM Modifications**: Nick Engmann
- **3D Design**: OnShape (https://bit.ly/raspi-onshape)
- **Hardware**: Raspberry Pi Foundation, HQ Camera

# Support

For questions or issues:
- [GitHub Issues](https://github.com/NickEngmann/piDSLM/issues)
- [Hackster Project Page](https://www.hackster.io/projects/2a86c3)

---

*Made with ❤️ for the Raspberry Pi community*
