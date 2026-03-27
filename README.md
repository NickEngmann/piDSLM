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
    ├── test_example.py         # GPIO and I2C hardware tests
    ├── test_dropbox_filters.py # Dropbox file filtering tests
    ├── conftest.py             # Test configuration with mocks
    └── embedded_mocks.py       # Hardware simulation mocks
>>>>>>> Stashed changes
```

You're then going to retrieve a Dropbox Access token to enable to Dropbox footage upload feature. To do this go ahead and [go to the Application Developer page on Dropbox](https://www.dropbox.com/developers/apps). Create an application and click the Generate Access Token button to generate your access token.

<<<<<<< Updated upstream
Then replace the dummy access token in Dropbox_upload.py with your new access token.
=======
The project includes a comprehensive test suite with hardware mocking:
>>>>>>> Stashed changes

```

# OAuth2 access token.  TODO: login etc.
TOKEN = 'YOUR_ACCESS_TOKEN'
```

<<<<<<< Updated upstream
Finally, run the INSTALL.sh script using the following command
=======
- **RPi.GPIO mocked**: Simulates GPIO pin control
- **I2C/SPI/UART mocked**: Hardware communication simulation
- **guizero mocked**: GUI framework simulation
- **Source loading**: Custom fixture loads and tests actual source files with while-True loops stripped
- **Auto-mocking**: Meta-path finder auto-mocks unknown hardware modules

### Test Coverage

- **Hardware tests** (`test_example.py`): 2 tests covering GPIO pin control and I2C communication
- **Dropbox filter tests** (`test_dropbox_filters.py`): 13 tests covering:
  - Dot file filtering (`.hidden_file`, `.gitignore`)
  - Temporary file filtering (`.tmp`, `.temp`, `@recycled`, `~backup`)
  - Generated file filtering (`.pyc`, `.pyo`)
  - Directory filtering (`__pycache__`)
  - Edge cases (empty strings, `None` values)
  - Normal file acceptance (`.jpg`, `.png`, `.pdf`, `.mp4`)
  - Argument parsing (`--count`, `--yes`, `--no` flags)

All 15 tests pass successfully in the mocked environment.
>>>>>>> Stashed changes

```
sudo ./INSTALL.sh
```



<<<<<<< Updated upstream
=======
- **Python 3.12+**
- **Pillow**: Image processing
- **guizero**: GUI framework
- **dropbox**: Dropbox API v2 SDK
- **RPi.GPIO**: Hardware control (production only)
- **raspistill/raspivid**: Camera utilities (production only)

Full dependency list: `requirements.txt` (Pillow, guizero, dropbox, guizero[images])

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

1. Verify TOKEN is set in `dropbox_upload.py`
2. Check internet connection
3. Review Dropbox app permissions

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

## License

This project is built on the MerlinPi foundation. Please respect the original project license and any third-party dependencies.

## Support

If you found this project useful, consider supporting the design work through [PayPal](https://paypal.me/nickengman).

For questions or contributions, please reach out via the [GitHub repository](https://github.com/NickEngmann/piDSLM).

---

*Designed for Raspberry Pi enthusiasts and DIY camera projects.*
>>>>>>> Stashed changes
