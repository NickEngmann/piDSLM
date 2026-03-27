# piDSLM - Raspberry Pi Digital Single Lens Mirrorless

Camera project for Raspberry Pi 2/3 + HQ Camera + MHS35-TFT

![piDSLM Design](https://i.imgur.com/VspFA5V.jpg)

## Introduction

Made an enclosure to host the [HQ Raspberry Pi Camera](https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/) as a standalone battery-powered DSLR that I'm calling piDSLM. Check out the links below for instructions on how to recreate the project!

The design includes a few modular camera grips for users. Feel free to make your own designs and reach out to me so I can include them!

### For More Info

- [Hackster](https://www.hackster.io/projects/2a86c3)
- [GitHub](https://github.com/NickEngmann/piDSLM)
- [Instructables](TBD)

Designed using [OnShape](https://bit.ly/raspi-onshape)

If you found this useful, please donate what you think it is worth to my [paypal.me](https://paypal.me/nickengman). Help cover the time of design.

Thanks, Enjoy!

## Project Structure

```
<<<<<<< Updated upstream

git clone https://github.com/NickEngmann/pidslm.git
cd pidslm
=======
piDSLM/
├── pidslm.py              # Main GUI application
├── dropbox_upload.py      # Dropbox sync utility with argparse
├── INSTALL.sh             # Installation script
├── pidslm.desktop         # Auto-start configuration
├── PiDSLR.fzz             # 3D enclosure design (Fusion 360)
├── icon/                  # UI icons (14 images)
├── requirements.txt       # Python dependencies
└── tests/                 # Test suite
    ├── test_example.py            # GPIO and I2C hardware tests
    ├── test_dropbox_filters.py    # Dropbox file filtering tests
    ├── test_dropbox_error_handling.py # Error handling tests
    ├── conftest.py                # Test configuration with mocks
    └── embedded_mocks.py          # Hardware simulation mocks
>>>>>>> Stashed changes
```

## Installation

<<<<<<< Updated upstream
Then replace the dummy access token in Dropbox_upload.py with your new access token.
=======
For the codebase, I built the piDSLM codebase off of a forked copy of fellow DIYer Martin Manders' [MerlinPi project](https://github.com/MisterEmm/MerlinPi). The piDSLM codebase is still in its infancy but it allows the user to take photos/videos, and view them in a gallery. It also allows users to bulk upload the footage to Dropbox.
>>>>>>> Stashed changes

### Step 1: Clone the Repository

SSH into your Raspberry Pi and run:

```bash
git clone https://github.com/NickEngmann/pidslm.git
cd pidslm
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

<<<<<<< Updated upstream
Finally, run the INSTALL.sh script using the following command
=======
### Step 3: Configure Dropbox Access Token

You'll need a Dropbox Access token to enable the Dropbox footage upload feature:

1. Go to the [Dropbox Application Developer page](https://www.dropbox.com/developers/apps)
2. Create an application
3. Click the "Generate Access Token" button to generate your access token
4. Replace the dummy token in `dropbox_upload.py`:
>>>>>>> Stashed changes

```python
# OAuth2 access token. TODO: login etc.
TOKEN = 'YOUR_ACCESS_TOKEN'  # Replace with your actual token
```

### Step 4: Run Installation Script

```bash
sudo ./INSTALL.sh
```

## Dependencies

### Runtime Dependencies

<<<<<<< Updated upstream
=======
- **Python 3.12+**
- **Pillow**: Image processing
- **guizero**: GUI framework
- **dropbox**: Dropbox API v2 SDK
- **RPi.GPIO**: Hardware control (production only)
- **raspistill/raspivid**: Camera utilities (production only)

Full dependency list: see `requirements.txt` (Pillow, guizero, dropbox, guizero[images])

## Testing

The project includes a comprehensive test suite with hardware mocking:

### Mock Infrastructure

- **RPi.GPIO mocked**: Simulates GPIO pin control with realistic constants (BCM/BOARD modes, HIGH/LOW levels)
- **I2C/SPI/UART mocked**: Hardware communication simulation
- **guizero mocked**: GUI framework simulation
- **Source loading**: Custom fixture loads and tests actual source files with `while-True` loops stripped
- **Auto-mocking**: Meta-path finder auto-mocks unknown hardware modules
- **Python 3.14 compatible**: Fixed deprecated `ast.NameConstant` usage in conftest.py

### Test Coverage

#### Hardware Tests (`test_example.py`) - 2 tests
- GPIO pin control simulation
- I2C communication testing

#### Dropbox Filter Tests (`test_dropbox_filters.py`) - 13 tests
- Dot file filtering (`.hidden_file`, `.gitignore`, `.DS_Store`)
- Temporary file filtering (`.tmp`, `.temp`, `@recycled`, `~backup`)
- Generated file filtering (`.pyc`, `.pyo`)
- Directory filtering (`__pycache__`)
- Edge cases (empty strings, `None` values)
- Normal file acceptance (`.jpg`, `.png`, `.pdf`, `.mp4`)
- Case-sensitive filtering

#### Error Handling Tests (`test_dropbox_error_handling.py`) - 8 tests
- Upload returns success dict with proper structure
- API error handling and response
- IO error handling and file read failures
- Nested path folder creation on errors
- Overwrite flag handling
- Case-sensitive file filtering
- Argument parsing with `--count` limit
- Invalid token detection

**All 23 tests pass successfully with no warnings in the mocked environment.**

### Running Tests

```bash
pytest tests/ -v
```

## Usage

### Main Application

```bash
python3 pidslm.py
```

### Dropbox Upload (Command Line)

```bash
python3 dropbox_upload.py [folder] [rootdir] [options]
```

**Arguments:**
- `folder`: Dropbox folder name (default: `Downloads`)
- `rootdir`: Local directory to upload (default: `~/Downloads`)

**Options:**
- `--token TOKEN`: Access token (required)
- `--yes`, `-y`: Answer yes to all questions
- `--no`, `-n`: Answer no to all questions
- `--default`, `-d`: Take default answer on all questions
- `--count N`: Maximum number of files to upload

**Example:**
```bash
python3 dropbox_upload.py MyBackup ~/Pictures --token YOUR_TOKEN --count 100
```

## Troubleshooting

### Camera not working

1. Check `/boot/config.txt` has `start_x=1` and `gpu_mem=128`
2. Verify camera is connected to CSI port 0
3. Run `vcgencmd get_camera` to check detection

### GPIO button not responding

1. Verify pin 16 wiring (BCM numbering)
2. Check for button bounce issues (currently set to 2500ms)
3. Ensure RPi.GPIO is not being used elsewhere

### Dropbox upload fails

1. Verify `TOKEN` is set in `dropbox_upload.py`
2. Check internet connection
3. Review Dropbox app permissions
4. Ensure the Dropbox folder exists or has write permissions

### Gallery not showing photos

1. Ensure photos are saved to `/home/pi/Downloads/`
2. Check file permissions on Downloads directory
3. Verify photo format is `.jpg`

## Design Notes

The piDSLM project is built as a fork of the [MerlinPi project](https://github.com/MisterEmm/MerlinPi) by Martin Manders. Key differences:

- Custom enclosure design (3D printable)
- MHS35-TFT display integration
- Enhanced GUI layout
- Bulk Dropbox upload feature
- GPIO button capture support
- Comprehensive test suite with hardware mocking

## Known Issues

- Requires Raspberry Pi hardware for full functionality
- Dropbox OAuth token must be configured (currently uses placeholder)
- GPIO operations need hardware or mocked environment
- INSTALL.sh requires root privileges and reboots the system
- No GitHub Actions workflows configured yet

## License

This project is built on the MerlinPi foundation. Please respect the original project license and any third-party dependencies.

## Support

If you found this project useful, consider supporting the design work through [PayPal](https://paypal.me/nickengman).

For questions or contributions, please reach out via the [GitHub repository](https://github.com/NickEngmann/piDSLM).

---

*Designed for Raspberry Pi enthusiasts and DIY camera projects.*
>>>>>>> Stashed changes
