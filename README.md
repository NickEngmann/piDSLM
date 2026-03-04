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

# Usage

The main application provides a GUI interface for camera control:

1. Launch the application: `python3 pidslm.py`
2. Use the on-screen buttons to:
   - Take photos
   - Record videos
   - View captured media in gallery
   - Upload footage to Dropbox

The interface is designed for the MHS35-TFT display on Raspberry Pi.

# Testing

Run the test suite using pytest:

```bash
python -m pytest tests/ -v
```

The tests use hardware mocks provided in `tests/conftest.py` for RPi.GPIO, guizero, and other hardware modules.

# Contributing

This project is inspired by the MerlinPi project. Feel free to:

- Submit bug reports and feature requests
- Contribute camera grip designs for the enclosure
- Share improvements to the codebase

For design contributions, reach out to the author for inclusion.

# License

This project is based on the MerlinPi project by Martin Manders. Please respect the original license and contributors.
