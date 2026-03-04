piDSLM - Raspberry Pi Digital Single Lens Mirrorless
===============

Camera project for Raspberry Pi 2/3 + HQ Camera + MHS35-TFT

![piDSLM](https://i.imgur.com/VspFA5V.jpg)

## Overview

piDSLM provides a DSLR-like interface for the Raspberry Pi HQ Camera with GPIO controls. The application features:

- Photo capture and video recording
- GPIO button controls for shutter and menu navigation
- MHS35-TFT display integration
- Dropbox cloud upload support
- Customizable camera settings

## Features

- **Camera Control**: Full DSLR-like interface for photo and video capture
- **GPIO Integration**: Physical button controls for shutter and menu navigation
- **Display Support**: Compatible with MHS35-TFT display
- **Cloud Storage**: Automatic Dropbox upload functionality
- **Custom Settings**: Adjustable camera parameters

## Installation

### Prerequisites

- Raspberry Pi 2 or 3 (or compatible hardware)
- Raspberry Pi HQ Camera
- MHS35-TFT display
- GPIO buttons for control

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/NickEngmann/piDSLM.git
   cd piDSLM
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the installation script (requires sudo):
   ```bash
   sudo bash INSTALL.sh
   ```

## Usage

### Running the Application

```bash
python3 pidslm.py
```

The application provides a GUI interface for:
- Capturing photos
- Recording videos
- Managing camera settings
- Uploading to Dropbox

### GPIO Controls

Physical buttons are connected to GPIO pins for:
- Shutter button (photo/video capture)
- Menu navigation buttons
- Settings adjustment

### Dropbox Integration

Upload photos and videos to Dropbox:
```bash
python3 dropbox_upload.py --yes
```

## Testing

### Running Tests

The project uses pytest with comprehensive hardware mocking for Raspberry Pi modules.

```bash
python3 -m pytest tests/ -v
```

### Test Infrastructure

- **conftest.py**: Auto-generates mocks for 15+ RPi hardware modules (RPi.GPIO, picamera, guizero, spidev, smbus, gpiozero, etc.)
- **embedded_mocks.py**: Contains MockGPIO, MockI2C, MockSPI, MockUART classes
- **Hardware mocking**: Required for running tests on non-RPi systems

### Test Requirements

Tests require the following to be mocked:
- RPi.GPIO for GPIO control
- picamera for camera operations
- guizero GUI components
- Other hardware interfaces (I2C, SPI, UART)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. For testing on non-RPi hardware, ensure conftest.py mocks are available
4. Run tests: `python3 -m pytest tests/ -v`

### Code Style

- Follow PEP 8 style guidelines
- Add tests for new features
- Document new functionality in README.md

## Dependencies

- Pillow: Image processing
- guizero: GUI framework
- dropbox: Cloud storage integration
- guizero[images]: Image handling extensions
- RPi.GPIO: GPIO control (mocked for testing)
- picamera: Camera operations (mocked for testing)

## Links

- [GitHub](https://github.com/NickEngmann/piDSLM)
- [Instructables](TBD)
- [OnShape Design](https://bit.ly/raspi-onshape)
- [PayPal Donations](https://paypal.me/nickengman)

## License

MIT License
