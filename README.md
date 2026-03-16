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

For the codebase, I built the piDSLM codebase off of a forked copy of fellow DIYer Martin Manders' [MerlinPi project](https://github.com/MisterEmm/MerlinPi). The piDSLM codebase allows the user to take photos/videos, view them in a gallery, and bulk upload footage to Dropbox.

### Hardware Requirements
- **Raspberry Pi 2/3/4** with 512MB+ RAM
- **Raspberry Pi HQ Camera** (or Camera Module v2)
- **3.5" TFT Display** (MHS35-TFT or compatible)
- **GPIO Button** for shutter activation
- **MicroSD Card** with Raspberry Pi OS (Bookworm/Jammy recommended)

### Software Dependencies
The following Python packages are required (see `requirements.txt`):
- `Pillow` (8.0+) — Image processing and manipulation
- `guizero` (1.4+) — Cross-platform GUI framework for Python
- `dropbox` (10.1+) — Dropbox API client for cloud uploads
- `RPi.GPIO` — Hardware GPIO control (Pi-only; mocked for testing)
- `picamera` / `picamera2` — Camera control (Pi-only; mocked for testing)

### Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/NickEngmann/pidslm.git
   cd pidslm
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Dropbox access**
   - Go to the [Dropbox Developers Console](https://www.dropbox.com/developers/apps)
   - Create a new app with "Full Dropbox" access
   - Generate an Access Token
   - Edit `dropbox_upload.py` and replace the token:
     ```python
     TOKEN = 'YOUR_ACCESS_TOKEN'  # Replace with your token from step above
     ```

4. **Run the installation script**
   ```bash
   sudo ./INSTALL.sh
   ```
   This sets up the application at `/home/pi/piDSLM/` and configures auto-start.

5. **Launch the application**
   ```bash
   python3 pidslm.py
   ```

## Features

### Camera Controls
The GUI provides six primary camera functions:

| Button | Function | Description |
|--------|----------|-------------|
| **Focus** | Long Preview | 15-second live preview to adjust focus |
| **Gallery** | Photo Gallery | Browse captured images with navigation |
| **HD 30s** | Video Capture | Record 30-second HD video |
| **Burst** | Burst Mode | Capture 10 photos with 1-second intervals |
| **1h 60pix** | Timelapse | Capture photos every 60s for 1 hour |
| **HD 30m** | Split Recording | 30-minute HD video split into 5-second segments |

### Additional Functions

- **Shutter Button** — GPIO pin 16 triggers instant photo capture on button press
- **Upload** — Bulk upload Downloads folder contents to Dropbox
- **Clear** — Delete all files in the Downloads folder

### Output Directory
Photos and videos are saved to `/home/pi/Downloads/` by default. This can be customized via the `HOME` environment variable or by modifying the `downloads_dir` configuration in `pidslm.py`.

## Testing

Run the test suite with pytest:

```bash
pytest tests/ -v
```

The test suite includes:
- `tests/test_example.py` — GPIO and I2C communication tests
- `tests/embedded_mocks.py` — Hardware simulation mocks
- `tests/conftest.py` — Auto-mocking for RPi modules

**Note**: Hardware tests use mocked modules (`RPi.GPIO`, `picamera`, etc.) to run on any Linux system.

## Project Structure

```
piDSLM/
├── pidslm.py              # Main GUI application
├── dropbox_upload.py      # Dropbox upload utility
├── INSTALL.sh             # Installation script
├── pidslm.desktop         # Auto-start desktop entry
├── PiDSLR.fzz             # 3D enclosure design (Fusion 360)
├── icon/                  # UI icons (PNG format)
│   ├── cam.png            # Camera/shutter icon
│   ├── gallery.png        # Gallery icon
│   ├── vid.png            # Video icon
│   ├── lapse.png          # Timelapse icon
│   ├── long.png           # Split recording icon
│   ├── drop.png           # Upload icon
│   ├── del.png            # Clear/delete icon
│   ├── prev.png           # Previous button
│   ├── self.png           # Shutter button
│   ├── left.png           # Gallery navigation ←
│   └── right.png          # Gallery navigation →
├── README.md              # This documentation
├── requirements.txt       # Python dependencies
└── tests/                 # Test suite
    ├── test_example.py
    ├── embedded_mocks.py
    └── conftest.py
```

## Contributing

This project is a fork of [MerlinPi](https://github.com/MisterEmm/MerlinPi) with enhancements for DSLR functionality. Contributions are welcome! Please consider:

- Adding new camera modes (slow motion, RAW capture)
- Improving gallery navigation
- Adding cloud storage options (Google Drive, OneDrive)
- Enhancing the 3D enclosure design

## Credits

- **Base Project**: [MerlinPi](https://github.com/MisterEmm/MerlinPi) by Martin Manders
- **3D Design**: Created using [OnShape](https://bit.ly/raspi-onshape)
- **Camera Hardware**: [Raspberry Pi HQ Camera](https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/)
- **Display**: MHS35-TFT 3.5" TFT LCD

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

*If you found this project useful, please consider donating to support development at [paypal.me/nickengman](https://paypal.me/nickengman).*



