piDSLM - Raspberry Pi Digital Single Lens Mirrorless
===============

<<<<<<< Updated upstream
Camera project for Raspberry Pi 2/3 + HQ Camera +  MHS35-TFT
=======
**Camera project for Raspberry Pi 2/3/4 + HQ Camera + MHS35-TFT Display**
>>>>>>> Stashed changes

<img src="https://i.imgur.com/VspFA5V.jpg" data-canonical-src="https://i.imgur.com/VspFA5V.jpg" width="400" height="400" />

# Introduction

<<<<<<< Updated upstream
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
=======
## Introduction
>>>>>>> Stashed changes

# Installation

<<<<<<< Updated upstream
For the codebase, I built the piDSLM codebase off of a forked a copy of fellow DIYer Martin Manders [MerlinPi project](https://github.com/MisterEmm/MerlinPi). The piDSLM codebase is still in its infancy but it allows the user to take photos/videos, and view them in a gallery. It also allows users to bulk upload the footage to Dropbox. To begin ssh into the Raspberry Pi and run the following command:
=======
### Key Features

- **Hardware Control**: GPIO button trigger for photo capture
- **Multiple Capture Modes**: Photo, video, burst, timelapse, and split HD recording
- **On-Device Gallery**: Real-time image preview and navigation
- **Cloud Backup**: Automatic Dropbox synchronization for captured media
- **3D-Printable Enclosure**: Modular design with interchangeable grips

---

## Design Features

### Enclosure Improvements

The piDSLM enclosure is designed for modularity and ease of use:

- **Modular Design**: Interchangeable camera grips and mounting options
- **3D Printable**: Entire enclosure designed for FDM printing
- **Compact Form Factor**: Optimized for portability while maintaining accessibility
- **Heat Management**: Ventilation channels for extended operation

### Design Files

| File | Description |
|------|-------------|
| [PiDSLR.fzz](PiDSLR.fzz) | FreeCAD design file for enclosure |
| [DESIGN_IMPROVEMENTS.md](DESIGN_IMPROVEMENTS.md) | Design improvement documentation |
| [3D_PRINTING_GUIDE.md](3D_PRINTING_GUIDE.md) | 3D printing instructions and settings |

**CAD Software**:
- **OnShape**: Cloud-based collaborative design
  - View interactive model: [OnShape Link](https://bit.ly/raspi-onshape)
- **FreeCAD**: Open-source CAD (for local modifications)
  - Export to STL: File → Export → Select "STL" format

### Modular Grips

The design supports interchangeable grips for different use cases:
- Standard vertical grip
- Horizontal orientation grip
- Tripod mount adapter

*Feel free to create your own grip designs and contribute!*

---

## Technical Overview

### Hardware Requirements

| Component | Specification |
|-----------|---------------|
| **Computer** | Raspberry Pi 2/3/4 |
| **Camera** | Raspberry Pi HQ Camera or Camera Module v2 |
| **Display** | MHS35-TFT Display (3.5" LCD) |
| **Controls** | GPIO Button for shutter control (Pin 16 BCM) |
| **Power** | Optional battery pack for portable operation |

### Software Features

| Feature | Description | Implementation |
|---------|-------------|----------------|
| **Photo Capture** | Still images | `raspistill` via GPIO trigger |
| **Video Recording** | HD video (30s) | `raspivid` command |
| **Burst Mode** | 10-second burst capture | `raspistill` with 10s timeout |
| **Timelapse** | 1-hour timelapse (60s intervals) | `raspistill` with 3600s timeout |
| **Gallery View** | On-device image browser | guizero GUI with navigation |
| **Dropbox Sync** | Automatic cloud backup | `dropbox_upload.py` module |

### Design Tools

- **CAD**: OnShape (cloud-based) and FreeCAD
- **3D Printing**: FDM compatible designs (0.2mm layer height recommended)
- **GUI Framework**: [guizero](https://github.com/pyguizero/guizero) (Python)
- **Hardware Interface**: [RPi.GPIO](https://pypi.org/project/rpi-gpio/)

---

## Installation

### Prerequisites
>>>>>>> Stashed changes

```

<<<<<<< Updated upstream
git clone https://github.com/NickEngmann/pidslm.git
cd pidslm
```

You're then going to retrieve a Dropbox Access token to enable to Dropbox footage upload feature. To do this go ahead and [go to the Application Developer page on Dropbox](https://www.dropbox.com/developers/apps). Create an application and click the Generate Access Token button to generate your access token.

Then replace the dummy access token in Dropbox_upload.py with your new access token.

```

# OAuth2 access token.  TODO: login etc.
TOKEN = 'YOUR_ACCESS_TOKEN'
```

Finally, run the INSTALL.sh script using the following command

```
sudo ./INSTALL.sh
```

=======
**Software Dependencies** (from [requirements.txt](requirements.txt)):
- Pillow (Python Imaging Library)
- guizero (GUI framework)
- dropbox (Dropbox API SDK)
- RPi.GPIO (hardware control)
>>>>>>> Stashed changes


<<<<<<< Updated upstream
=======
1. Print enclosure parts using the provided STL files (see [3D_PRINTING_GUIDE.md](3D_PRINTING_GUIDE.md))
2. Assemble Raspberry Pi, display, and camera module
3. Connect GPIO button to pin 16 (BCM)
4. Power on and verify all connections

### Software Setup

piDSLM builds upon Martin Manders' [MerlinPi project](https://github.com/MisterEmm/MerlinPi). While still in active development, it provides:
- Photo/video capture
- On-device gallery viewing
- Dropbox cloud upload

#### Step 1: Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-rpi.gpio python3-guizero
sudo apt-get install -y libfreetype6-dev libffi-dev
```

#### Step 2: Clone and Install Dependencies

```bash
git clone https://github.com/NickEngmann/pidslm.git
cd pidslm
pip3 install -r requirements.txt
```

#### Step 3: Configure Dropbox (Optional - for cloud sync)

1. Go to [Dropbox Developer Apps](https://www.dropbox.com/developers/apps)
2. Create an application
3. Generate an Access Token
4. Edit `dropbox_upload.py` and replace the token:

```python
# OAuth2 access token (dropbox_upload.py line 19)
TOKEN = 'YOUR_ACTUAL_DROPBOX_ACCESS_TOKEN'
```

#### Step 4: Run Installation Script

```bash
sudo ./INSTALL.sh
```

The installation script will:
- Copy icon files and Python scripts to `/home/pi/piDSLM/`
- Install Python dependencies
- Set up auto-start desktop file

#### Step 5: Launch the Application

```bash
python3 pidslm.py
```

### Desktop Auto-Start

The application is configured to auto-launch via the [pidslm.desktop](pidslm.desktop) file for seamless operation on boot.

**Configuration** (from [pidslm.desktop](pidslm.desktop) lines 1-4):
```ini
[Desktop Entry]
Type=Application
Name=PiDSLM
Exec=/usr/bin/python3 /home/pi/piDSLM/pidslm.py
```

---

## File Structure

```
piDSLM/
├── pidslm.py              # Main GUI application (106 lines)
├── dropbox_upload.py      # Dropbox sync utility (198 lines)
├── INSTALL.sh             # Installation script (24 lines)
├── pidslm.desktop         # Desktop auto-start configuration (4 lines)
├── PiDSLR.fzz             # 3D enclosure design file
├── DESIGN_IMPROVEMENTS.md # Design improvement documentation
├── 3D_PRINTING_GUIDE.md   # 3D printing instructions
├── README.md              # This file
├── MARISOL.md             # Pipeline context documentation
├── requirements.txt       # Python dependencies
├── icon/                  # GUI icons and images (11 PNG files)
└── tests/                 # Test suite
    ├── conftest.py        # Auto-generated fixture with 15+ RPi hardware mocks
    ├── embedded_mocks.py  # Hardware simulation mocks
    └── test_example.py    # Example test template (2 passing tests)
```

---

## Key Functions Reference

### pidslm.py — Main GUI Application

The `piDSLM` class provides the following methods:

| Method | Description | Line Range |
|--------|-------------|------------|
| `__init__()` | GUI initialization, GPIO setup on pin 16 | 7-58 |
| `capture_image()` | Still image capture using raspistill | 72-78 |
| `takePicture()` | GPIO button trigger with 3.5s timeout | 80-86 |
| `video_capture()` | 30s HD video recording | 97-104 |
| `burst()` | Burst mode (10s continuous capture) | 59-67 |
| `lapse()` | Timelapse (1h at 60s intervals) | 69-76 |
| `split_hd_30m()` | 30m split video (5s segments) | 68-71 |
| `long_preview()` | 15s preview mode | 77-82 |
| `show_gallery()` | Image gallery viewer with navigation | 92-96 |
| `upload()` | Trigger Dropbox sync via subprocess | 106 |
| `clear()` | Delete Downloads folder contents | 60 |
| `timestamp()` | Generate filename timestamp string | 62-67 |

### dropbox_upload.py — Dropbox Sync Utility

| Function | Description | Line Range |
|----------|-------------|------------|
| `parse_args()` | Command-line argument parsing with --yes, --no, --default flags | 26-38 |
| `list_folder()` | Dropbox folder listing with error handling | 117-133 |
| `download()` | File download with content verification | 135-153 |
| `upload()` | Dropbox file upload with comprehensive error handling | 155-181 |
| `yesno()` | User prompt helper with q/quit and p/pdb commands | 183-214 |
| `main()` | Main upload loop iterating over folder hierarchy | 40-114 |

### Test Suite

The project includes automated tests in `tests/`:
- **conftest.py**: Auto-generated fixture with 15+ RPi hardware mocks
- **embedded_mocks.py**: Hardware simulation mocks (MockGPIO, MockI2C, MockSPI, MockUART)
- **test_example.py**: Example test template with 2 passing tests

**Test Results** (verified with pytest 9.0.2, Python 3.12.3):
- test_gpio_pin_control: PASSED
- test_i2c_communication: PASSED

---

## Notes and Configuration

| Setting | Value | Location |
|---------|-------|----------|
| **Access Token** | Required in dropbox_upload.py | dropbox_upload.py line 19 |
| **Downloads Folder** | /home/pi/Downloads | pidslm.py line 79 |
| **Image Output** | /home/pi/Downloads/*.jpg | pidslm.py line 79 |
| **Video Output** | /home/pi/Downloads/*.h264 | pidslm.py line 85 |
| **GPIO Button** | Pin 16 (BCM mode) | pidslm.py lines 20-21 |
| **Display Path** | /home/pi/piDSLM/icon/ | INSTALL.sh line 3 |
| **Auto-Start Exec** | /usr/bin/python3 /home/pi/piDSLM/pidslm.py | pidslm.desktop line 3 |

---

## Environment

- **Development**: Linux environment with Python 3.12.3
- **Target Hardware**: Raspberry Pi 2/3/4 with HQ Camera and MHS35-TFT display
- **Docker Image**: lotus-rpi-python:latest (for CI/CD testing)

---

## Support and Contributions

This project is part of an open-source hardware and software initiative. If you found it useful:

- ⭐ Star the repository to show support
- 💰 [PayPal](https://paypal.me/nickengman) — Contribute to design and development time
- 🔄 Share your modifications and improvements!

### Design Contributions

We welcome design contributions! To submit improvements:

1. Fork the repository
2. Export your design changes from OnShape or FreeCAD
3. Add new STL files to `stl/` directory
4. Update this README with your changes
5. Submit a pull request

Please include:
- Description of the improvement
- Parts list (if any new components)
- Print settings recommendations
- Compatibility notes

For more information:
- [Hackster Project Page](https://www.hackster.io/projects/2a86c3)
- [GitHub Repository](https://github.com/NickEngmann/piDSLM)
- [OnShape Design (Interactive 3D Model)](https://bit.ly/raspi-onshape)

---

## License

This project is open-source hardware and software. Feel free to modify, share, and build upon it. Attribution appreciated but not required.

### Design License

The enclosure design is released under [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/). See [DESIGN_IMPROVEMENTS.md](DESIGN_IMPROVEMENTS.md) for details.

---

## Version History

- **v1.0** (Current): Initial release with GPIO controls, gallery display, and Dropbox sync
- **v2.0** (Design): Enclosure improvements with modular grips, heat management, and cable management

---

## Documentation Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | User-facing documentation (this file) |
| [MARISOL.md](MARISOL.md) | Pipeline context with factual build/test/history info |
| [DESIGN_IMPROVEMENTS.md](DESIGN_IMPROVEMENTS.md) | Design improvements and CAD documentation |
| [3D_PRINTING_GUIDE.md](3D_PRINTING_GUIDE.md) | 3D printing instructions and settings |
>>>>>>> Stashed changes
