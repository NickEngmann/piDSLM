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



<<<<<<< Updated upstream
=======
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

Then replace the dummy access token in Dropbox_upload.py with your new access token.

```

# OAuth2 access token.  TODO: login etc.
TOKEN = 'YOUR_ACCESS_TOKEN'
```

Finally, run the INSTALL.sh script using the following command

```
sudo ./INSTALL.sh
```

# Features

## Camera Controls

The piDSLM application provides a comprehensive GUI with multiple camera functions:

- **Focus Preview**: 15-second live preview for focusing (line 74 in pidslm.py)
- **Gallery View**: Browse captured photos and videos (line 91 in pidslm.py)
- **Video Capture**: Record 30-second HD video clips (line 98 in pidslm.py)
- **Burst Mode**: Capture up to 10,000 images in rapid succession (line 59 in pidslm.py)
- **Timelapse**: Capture 60 images over 1 hour with 60-second intervals (line 66 in pidslm.py)
- **Split HD**: Record 30-minute videos in 5-second segments (line 71 in pidslm.py)
- **Upload to Dropbox**: Bulk upload all footage from Downloads folder (line 107 in pidslm.py)
- **Clear Folder**: Remove all files from Downloads directory (line 52 in pidslm.py)

## GPIO Button Control

A physical button connected to GPIO pin 16 triggers photo capture automatically (line 15-16 in pidslm.py):

- Uses BCM GPIO numbering scheme
- FALLING edge detection with 2500ms bouncetime
- Automatically timestamps and saves photos to /home/pi/Downloads/

## Hardware Requirements

- **Raspberry Pi**: Model 2 or Model 3 recommended
- **Camera**: Raspberry Pi High Quality (HQ) Camera
- **Display**: 3.5" TFT display (MHS35-TFT)
- **GPIO**: 40-pin header for button connection
- **Storage**: microSD card with sufficient space for photos/videos

# Technical Details

## Project Structure

```
piDSLM/
├── pidslm.py          # Main application (134 lines)
├── dropbox_upload.py  # Dropbox sync utility (158 lines)
├── INSTALL.sh         # Installation script (16 lines)
├── pidslm.desktop     # Auto-start configuration
├── PiDSLR.fzz         # 3D enclosure design (Fusion 360)
├── icon/              # UI icons (14 PNG files)
└── tests/             # Test suite
    ├── test_example.py     # Hardware test examples
    ├── conftest.py         # Test configuration
    └── embedded_mocks.py   # Hardware mocks
```

## Dependencies (from requirements.txt)

| Package | Purpose |
|---------|---------|
| Pillow | Image processing and display |
| guizero | GUI framework for camera controls |
| dropbox | Dropbox API integration for uploads |
| guizero[images] | Additional image support |

## Key File Locations

- **Application**: `/home/pi/piDSLM/pidslm.py` (line 7)
- **Upload Script**: `/home/pi/piDSLM/dropbox_upload.py` (line 19)
- **Captured Media**: `/home/pi/Downloads/`
- **Icons Directory**: `/home/pi/piDSLM/icon/`

# Testing

## Run Tests

Execute the test suite using pytest:

```bash
python3 -m pytest tests/ -v
```

## Current Test Coverage

The test suite includes 27 tests across 3 test files:

### Configuration Tests (test_config.py - 8 tests)
- **test_default_config**: Verifies default configuration values
- **test_config_from_env**: Tests environment variable configuration loading
- **test_get_icon_path**: Tests icon path resolution
- **test_get_capture_output_path**: Tests capture output path resolution
- **test_get_config_default**: Tests default config retrieval
- **test_set_config**: Tests global configuration setting
- **test_environment_variables_not_set**: Tests behavior when no env vars set
- **test_capture_settings_defaults**: Tests capture timing settings

### Dropbox Upload Tests (test_dropbox_upload.py - 15 tests)
- **test_parse_arguments_yes_flag**: Tests argument parsing
- **test_skip_dot_files**: Verifies dot files are skipped
- **test_skip_temporary_files**: Tests temporary file handling
- **test_list_folder_success**: Tests successful folder listing
- **test_list_folder_api_error**: Tests API error handling
- **test_upload_success**: Tests file upload functionality
- **test_download_success**: Tests file download functionality
- **test_download_error**: Tests download error handling
- **test_yesno_***: Tests interactive yes/no prompts (5 tests)
- **test_stopwatch_context_manager**: Tests timing context manager
- **test_main_invalid_folder_type**: Tests error handling for invalid folder
- **test_main_folder_not_exist**: Tests error handling for missing folder

### Hardware Mock Tests (test_example.py - 2 tests)
- **test_gpio_pin_control**: Tests GPIO pin output (HIGH/LOW state control)
- **test_i2c_communication**: Tests I2C bus read/write operations

## Hardware Mocking

The test suite uses `embedded_mocks.py` to simulate Raspberry Pi hardware:

- **MockGPIO**: Simulates RPi.GPIO pin control
- **MockI2C**: Simulates I2C bus communication
- **MockSPI**: Simulates SPI bus communication
- **MockUART**: Simulates UART serial communication

## Test Configuration

`conftest.py` provides:

- Auto-mocking of 15+ Raspberry Pi hardware modules
- `source_module` fixture for loading project code with while-True loops stripped
- Realistic GPIO constants (BCM=11, HIGH=1, LOW=0, etc.)

## Configuration Module

The `config.py` module provides centralized configuration management:

### PiDSLMConfig Class

A dataclass that stores all configuration options:

```python
# Default values
from config import PiDSLMConfig, get_config, set_config

cfg = PiDSLMConfig()
cfg.downloads_dir  # "~/Downloads"
cfg.icon_dir       # "./icon"
cfg.dropbox_enabled  # False
cfg.dropbox_token    # None
cfg.button_pin       # 16
cfg.button_mode      # "BCM"
```

### Configuration via Environment Variables

```bash
export PIDSLM_DOWNLOADS_DIR="/custom/path/Downloads"
export PIDSLM_ICON_DIR="/custom/icons"
export DROPBOX_ACCESS_TOKEN="your_token_here"
```

Then load from environment:
```python
from config import PiDSLMConfig
cfg = PiDSLMConfig.from_env()
```

### Global Configuration Management

```python
from config import get_config, set_config, PiDSLMConfig

# Get current config
cfg = get_config()

# Set custom config
custom_cfg = PiDSLMConfig(downloads_dir="/custom/path")
set_config(custom_cfg)
```

### Helper Methods

- `cfg.get_icon_path(icon_name)`: Returns full path to icon file
- `cfg.get_capture_output_path(filename)`: Returns full path to capture output

# Troubleshooting

## Dropbox Upload Issues

1. **Error**: "TOKEN is mandatory"
   - **Solution**: Ensure TOKEN variable is set in dropbox_upload.py (line 19)
   
2. **Error**: "Folder listing failed"
   - **Solution**: Check Dropbox API permissions and token validity

3. **Error**: "does not exist on your filesystem"
   - **Solution**: Verify /home/pi/Downloads/ directory exists

## GPIO Button Not Working

1. **Check Wiring**: Ensure button connects GPIO pin 16 to GND
2. **Check Permissions**: Run with sudo or add user to gpio group
3. **Verify Mode**: Check `GPIO.setmode(GPIO.BCM)` is used (line 13)

## Gallery Display Issues

1. **Error**: "saved_pictures list empty"
   - **Solution**: Ensure .jpg files exist in /home/pi/Downloads/
   
2. **Error**: "Picture not found"
   - **Solution**: Verify file path matches glob pattern `/home/pi/Downloads/*.jpg`

## Hardware Not Detected

1. **Camera Not Found**: Run `vcgencmd get_camera` to verify detection
2. **GPIO Issues**: Check `ls /sys/class/gpio/` for exported pins
3. **Display Issues**: Verify /boot/config.txt has `start_x=1` and `gpu_mem=128` (INSTALL.sh line 14)

# Contributing

This project is a fork of [MerlinPi](https://github.com/MisterEmm/MerlinPi) by Martin Manders. Features include:

- Enhanced enclosure design (PiDSLR.fzz)
- Dropbox integration for automated uploads
- Custom GPIO button triggers
- Timelapse and burst mode improvements

# License

Based on the MerlinPi project. This fork adds custom features and is distributed under the same terms.

# Known Issues

- **Hardware Dependency**: Requires Raspberry Pi hardware for full functionality
- **Dropbox Token**: OAuth token must be configured via `DROPBOX_ACCESS_TOKEN` environment variable or in dropbox_upload.py (line 26)
- **GPIO Operations**: Need hardware or mocked environment for testing
- **Hardcoded Paths**: pidslm.py uses hardcoded paths (`/home/pi/piDSLM/`, `/home/pi/Downloads/`) - use config.py environment variables for customization
- **Continuous Integration**: No GitHub Actions workflows configured yet
- **Display Compatibility**: Full-screen mode in guizero may have issues on non-native screens

# Credits

- **Original Project**: Martin Manders (MerlinPi)
- **Fork Author**: Nick Engmann (piDSLM)
- **Hardware**: Raspberry Pi Foundation, Pimoroni (MHS35-TFT)
- **Design**: OnShape (cloud-based CAD platform)
>>>>>>> Stashed changes
