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
- [Instructables] ( TBD )

Designed using
- [OnShape](https://bit.ly/raspi-onshape)

If you found this useful, please donate what you think it is worth to my [paypal.me](https://paypal.me/nickengman). Help cover the time of design.

Thanks, Enjoy!

# Features

- **Photo Capture**: Take high-quality photos with the HQ Camera
- **Video Recording**: Record video footage
- **Gallery View**: Browse captured photos and videos on the MHS35-TFT display
- **Dropbox Upload**: Bulk upload footage to Dropbox cloud storage
- **Battery Powered**: Standalone operation with portable power

# Installation

## Prerequisites

- Raspberry Pi 2 or 3
- Raspberry Pi HQ Camera
- MHS35-TFT display
- Python 3.12
- guizero (GUI framework)
- dropbox (for cloud uploads)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/NickEngmann/pidslm.git
cd pidslm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Dropbox access token:
   - Go to the [Dropbox Developer Console](https://www.dropbox.com/developers/apps)
   - Create an application
   - Click "Generate Access Token" to create your token
   - Edit `dropbox_upload.py` and replace the token:

```python
# OAuth2 access token
TOKEN = 'YOUR_ACCESS_TOKEN_HERE'
```

4. Run the installation script:
```bash
sudo ./INSTALL.sh
```

# Usage

## Running the Application

```bash
python3 pidslm.py
```

The application provides a GUI with the following controls:

- **Take Photo**: Captures an image to the Downloads folder
- **Start Video**: Begins video recording
- **Stop Video**: Ends video recording
- **View Gallery**: Opens a window to browse captured media
- **Upload to Dropbox**: Bulk uploads all media from Downloads to Dropbox

## File Locations

- Photos and videos are saved to: `/home/pi/Downloads/`
- Application logs: `/home/pi/piDSLM/logs/`
- Configuration: See `dropbox_upload.py` for Dropbox settings

# Testing

## Running Tests

The project uses pytest for testing with hardware mocks:

```bash
pytest tests/ -v
```

Tests are located in the `tests/` directory:
- `test_example.py`: Example test template
- `embedded_mocks.py`: Hardware simulation (RPi.GPIO, I2C, SPI, UART)
- `conftest.py`: Test configuration with auto-mocked hardware modules

## Mocked Hardware

Tests run in a containerized environment with mocked hardware:
- RPi.GPIO: Mocked for GPIO pin control
- I2C: Mocked for I2C bus communication
- SPI: Mocked for SPI communication
- UART: Mocked for serial communication
- guizero: Mocked for GUI components

# Project Structure

```
piDSLM/
├── pidslm.py          # Main application with GUI controls
├── dropbox_upload.py  # Dropbox upload functionality
├── INSTALL.sh         # Installation script
├── requirements.txt   # Python dependencies
├── tests/
│   ├── test_example.py
│   ├── embedded_mocks.py
│   └── conftest.py
└── README.md          # This file
```

# Known Issues

- Requires Raspberry Pi hardware for full functionality
- Dropbox OAuth token must be configured in `dropbox_upload.py`
- GPIO operations need hardware or mocked environment

# License

This project is built on Martin Manders' [MerlinPi project](https://github.com/MisterEmm/MerlinPi). See original project for licensing details.

# Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
