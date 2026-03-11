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

The main application (`pidslm.py`) provides a graphical interface for:

- Taking photos and videos
- Viewing captured media in a gallery
- Uploading footage to Dropbox

## Starting the Application

```bash
python3 pidslm.py
```

## Gallery

The gallery displays images from `/home/pi/Pictures/` directory. Navigate through captured media using the touchscreen interface.

## Dropbox Upload

To enable Dropbox uploads, configure your OAuth2 access token in `dropbox_upload.py`:

```python
TOKEN = 'YOUR_ACTUAL_ACCESS_TOKEN'
```

Generate your token from the [Dropbox Developer Console](https://www.dropbox.com/developers/apps).

# Testing

The project uses pytest for testing with hardware mocks for Raspberry Pi components.

## Running Tests

```bash
pytest tests/ -v
```

## Test Infrastructure

- **Hardware Mocks**: `conftest.py` auto-generates mocks for 15+ RPi modules (RPi.GPIO, I2C, SPI, UART, etc.)
- **Mock Classes**: `embedded_mocks.py` provides `MockGPIO`, `MockI2C`, `MockSPI`, `MockUART`
- **Test Template**: `tests/test_example.py` shows how to write tests using the mocks

## Example Test

```python
from embedded_mocks import MockGPIO

def test_gpio_pin_control():
    gpio = MockGPIO()
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUTPUT)
    gpio.output(17, gpio.HIGH)
    assert gpio.input(17) == gpio.HIGH
```

# Contributing

## Design Contributions

The project uses modular camera grips designed in [OnShape](https://bit.ly/raspi-onshape). Feel free to create your own designs and share them.

## Code Contributions

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Dependencies

- **Pillow**: Image processing
- **guizero**: GUI framework
- **dropbox**: Dropbox API integration
- **RPi.GPIO**: Hardware control (requires Raspberry Pi or mocked environment)

# License

This project is based on the [MerlinPi project](https://github.com/MisterEmm/MerlinPi) by Martin Manders.

# Support

If you found this project useful, consider donating via [paypal.me/nickengman](https://paypal.me/nickengman) to help cover design time.

# Links

- [Hackster Project Page](https://www.hackster.io/projects/2a86c3)
- [GitHub Repository](https://github.com/NickEngmann/piDSLM)
- [OnShape Design](https://bit.ly/raspi-onshape)
