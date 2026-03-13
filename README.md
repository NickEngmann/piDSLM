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


Designed using
- [OnShape](https://bit.ly/raspi-onshape)

If you found this useful, please donate what you think it is worth to my [paypal.me](https://paypal.me/NickEngmann). Help cover the time of design.

Thanks, Enjoy!

# Installation

For the codebase, I built the piDSLM codebase off of a forked a copy of fellow DIYer Martin Manders [MerlinPi project](https://github.com/MisterEmm/MerlinPi). The piDSLM codebase is still in its infancy but it allows the user to take photos/videos, and view them in a gallery. It also allows users to bulk upload the footage to Dropbox. To begin ssh into the Raspberry Pi and run the following command:

```

git clone https://github.com/NickEngmann/pidslm.git
cd pidslm
```

You're then going to retrieve a Dropbox Access token to enable to Dropbox footage upload feature. To do this go ahead and [go to the Application Developer page on Dropbox](https://www.dropbox.com/developers/apps). Create an application and click the Generate Access Token button to generate your access token.

Then replace the dummy access token in dropbox_upload.py with your new access token.

```

# OAuth2 access token.  TODO: login etc.
TOKEN = 'YOUR_ACCESS_TOKEN'
```

Finally, run the INSTALL.sh script using the following command

```
sudo ./INSTALL.sh
```

## Dependencies

Install Python dependencies using pip:

```bash
pip install -r requirements.txt
```

Required packages:
- Pillow (image processing)
- guizero (GUI framework)
- dropbox (cloud storage)
- guizero[images] (image support)

## Usage

Run the main application:

```bash
python3 pidslm.py
```

The application provides:
- Photo capture mode
- Video recording mode
- Gallery view for browsing media
- Dropbox upload functionality
- Time-lapse photography

## Testing

Run the test suite with pytest:

```bash
pytest tests/ -v
```

### Test Infrastructure

Tests use embedded hardware mocks for Raspberry Pi components:
- RPi.GPIO (GPIO pin simulation)
- I2C bus simulation
- SPI bus simulation
- UART serial simulation
- guizero GUI mocks

The mock system is auto-configured via `tests/conftest.py` which loads `tests/embedded_mocks.py`.

## Hardware Requirements

- Raspberry Pi 2 or 3
- HQ Camera Module
- MHS35-TFT Display
- GPIO pins for camera control

## Installation Script

The INSTALL.sh script performs:
1. Creates /home/pi/piDSLM directory
2. Copies application files (pidslm.py, dropbox_upload.py)
3. Copies icon directory
4. Installs desktop entry for autostart
5. Configures /boot/config.txt for camera support
6. Reboots the system

## 3D Printing

The enclosure design is available in `PiDSLR.fzz` (Fusion 360 format). Design was created using OnShape.

## Contributing

This project is based on the MerlinPi fork by MisterEmm. Feel free to contribute camera grip designs or improvements to the codebase.

## License

This project is open source. See the original MerlinPi project for licensing details.

## Support

For questions or issues, please open a GitHub issue or reach out through the project channels.




