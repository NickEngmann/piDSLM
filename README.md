piDSLM - Raspberry Pi Digital Single Lens Mirrorless
===============

Camera project for Raspberry Pi 2/3 + HQ Camera +  MHS35-TFT

<img src="https://i.imgur.com/VspFA5V.jpg" data-canonical-src="https://i.imgur.com/VspFA5V.jpg" width="400" height="400" />

# Introduction

Made an enclosure to host the [HQ Raspberry Pi Camera](https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/) as a standalone battery-powered DSLM that I'm calling piDSLM. Check out the links below for instructions on how to recreate the project!

The design includes a few modular camera grips for users. Feel free to make your own designs and reach out to me so I can include them!

For More Info:

- [Hackster](https://www.hackster.io/projects/2a86c3)
- [GitHub](https://github.com/NickEngmann/piDSLM)
- [Instructables] ( TBD )

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

Then replace the dummy access token in dropbox_upload.py with your new access token:

```python
# OAuth2 access token. TODO: login etc.
TOKEN = 'YOUR_ACCESS_TOKEN'  # dropbox_upload.py line 19
```

Finally, run the INSTALL.sh script using the following command:

```
sudo ./INSTALL.sh
```

# Features

## Capture Modes

The piDSLM provides multiple capture modes for different photography needs:

- **Manual Capture** - Press button or use Focus button for single shot (3.5s timeout)
- **Burst Mode** - Continuous capture for 10 seconds with 5-second intervals between shots
- **Timelapse** - Capture photos every 60 seconds for up to 1 hour
- **HD Video** - Record 30-second HD video clips
- **Split HD Video** - Record up to 30 minutes with 5-second segments automatically split
- **Long Preview** - 15-second preview mode for framing shots

## Gallery View

- Browse captured images in a full gallery window
- Navigate through images using left/right arrows
- Auto-detects all JPG files in the Downloads folder

## Dropbox Integration

- Upload photos and videos to Dropbox automatically
- Skip temporary files (dotfiles, py files, temp files)
- Compare file modification times to avoid redundant uploads
- Interactive prompts for file upload decisions
- Batch upload via command-line flags

# Hardware Requirements

- Raspberry Pi 2/3/4
- Raspberry Pi HQ Camera
- MHS35-TFT Display (3.5-inch TFT LCD)
- GPIO button connected to pin 16 (BCM numbering)
- Power supply for battery operation
- 3D printed enclosure (PiDSLR.fzz design file)

# Software Dependencies

See `requirements.txt` for the complete list of Python dependencies:

- Pillow - Image processing and manipulation
- guizero - Graphical user interface framework
- dropbox - Dropbox API SDK for file uploads
- guizero[images] - Image support for guizero widgets

# File Structure

```
piDSLM/
├── pidslm.py              # Main GUI application (167 lines)
├── dropbox_upload.py      # Dropbox sync utility (273 lines)
├── INSTALL.sh             # Installation script (17 lines)
├── pidslm.desktop         # Desktop auto-start configuration (5 lines)
├── PiDSLR.fzz             # 3D enclosure design (Fusion 360)
├── requirements.txt       # Python dependencies (4 lines)
├── README.md              # This documentation file
├── MARISOL.md             # Pipeline context documentation
├── icon/                  # GUI icon assets
│   ├── cam.png            # Capture button icon
│   ├── gallery.png        # Gallery button icon
│   ├── drop.png           # Dropbox upload icon
│   ├── del.png            # Clear folder icon
│   ├── prev.png           # Preview button icon
│   ├── vid.png            # Video capture icon
│   ├── lapse.png          # Timelapse icon
│   ├── long.png           # Long preview icon
│   ├── self.png           # Self-timer icon
│   ├── 100black.png       # 100% zoom icon
│   └── 100trans.png       # 100% transparent icon
└── tests/                 # Test suite
    ├── conftest.py        # Hardware mocks and fixtures (176 lines)
    ├── embedded_mocks.py  # Mock hardware classes
    └── test_example.py    # Example test cases
```

# Usage Guide

## Starting the Application

After installation, the application will automatically start when the Raspberry Pi boots. The main window displays a grid of buttons:

| Button | Function |
|--------|----------|
| Focus | 15-second live preview mode |
| Gallery | View all captured images |
| HD 30s | Record 30-second HD video |
| Burst | Continuous capture for 10 seconds |
| 1h 60pix | Timelapse: 1 hour at 60-second intervals |
| HD 30m in 5s | Split video: 30 minutes in 5-second segments |
| Upload | Bulk upload to Dropbox |
| Clear Folder | Delete all files in Downloads folder |

## GPIO Button Trigger

The physical button connected to GPIO pin 16 (BCM) automatically triggers photo capture when pressed. The button has a 2.5-second bounce time to prevent accidental double triggers.

## File Storage Locations

- **Images**: `/home/pi/Downloads/*.jpg`
- **Videos**: `/home/pi/Downloads/*.h264`
- **Burst mode**: `/home/pi/Downloads/BRYYYYMMDD_HHMMSS%04d.jpg`
- **Timelapse**: `/home/pi/Downloads/TLYYYYMMDD_HHMMSS%04d.jpg`
- **Split video**: `/home/pi/Downloads/YYYYMMDD_HHMMSSvid%04d.h264`

# Command-Line Options (dropbox_upload.py)

The Dropbox upload script supports the following options:

```
usage: dropbox_upload.py [-h] [--token TOKEN] [--yes] [--no] [--default]
                         [folder] [rootdir]

positional arguments:
  folder       Folder name in your Dropbox (default: Downloads)
  rootdir      Local directory to upload (default: ~/Downloads)

optional arguments:
  -h, --help   Show this help message and exit
  --token TOKEN
               Access token for Dropbox API
  --yes, -y    Answer yes to all questions
  --no, -n     Answer no to all questions
  --default, -d
               Take default answer on all questions
```

# Testing

Run the test suite with pytest:

```bash
cd tests/
python3 -m pytest -v
```

Current test coverage:
- GPIO pin control (test_gpio_pin_control)
- I2C communication simulation (test_i2c_communication)

The test framework uses mock hardware modules to enable testing without physical Raspberry Pi hardware.

# Troubleshooting

## GPIO Button Not Working

- Check that the button is connected to GPIO pin 16 (BCM)
- Verify wiring is correct (button between GPIO pin and ground)
- Check that RPi.GPIO module is properly installed

## Dropbox Upload Fails

- Ensure TOKEN in dropbox_upload.py is set to a valid access token
- Verify internet connectivity on the Raspberry Pi
- Check Dropbox API permissions for the configured app

## Gallery Won't Load

- Ensure JPG files exist in /home/pi/Downloads/
- Check file permissions for the Downloads directory
- Verify guizero image loading is working

# Development

## Running Without Installation

To test the application without full installation:

```bash
python3 pidslm.py
```

Note: This requires the icon directory and dependencies to be available.

## Modifying the Application

Key files to modify:
- `pidslm.py` - Main application logic and GUI
- `dropbox_upload.py` - Dropbox synchronization logic
- `INSTALL.sh` - Installation and setup process

# License

This project is based on the MerlinPi project. See the original repository for licensing information.

# Contributing

The design includes modular camera grips for users. Feel free to create your own 3D designs and reach out to the author for inclusion in the project.

# Credits

- **Original Concept**: Nick Engmann
- **Base Code**: Martin Manders (MerlinPi project)
- **Design Software**: OnShape
- **Camera**: Raspberry Pi HQ Camera
- **Display**: MHS35-TFT LCD

---

*Last updated: 2026-03-30*
*Documentation version: 1.2*
