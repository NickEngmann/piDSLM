# piDSLM - Raspberry Pi Digital Single Lens Mirrorless

![piDSLM Interface](https://i.imgur.com/VspFA5V.jpg)

A standalone battery-powered DSLM camera interface for Raspberry Pi 2/3 with HQ Camera and MHS35-TFT display.

## Features

- **Photo Capture**: Take high-quality photos using the Raspberry Pi HQ Camera
- **Video Recording**: Record HD video (30s clips) or split 30-minute sessions
- **Timelapse**: Capture timelapse photos with 60-second intervals over 1 hour
- **Burst Mode**: Capture rapid sequential photos (up to 10,000ms)
- **Gallery View**: Browse captured photos with left/right navigation
- **Long Preview**: 15-second preview mode
- **Dropbox Upload**: Bulk upload footage to Dropbox cloud storage
- **GPIO Control**: Button-activated photo capture with pin 16
- **Clear Function**: Delete all files from Downloads folder

## Project Links

- [Hackster](https://www.hackster.io/projects/2a86c3)
- [GitHub](https://github.com/NickEngmann/piDSLM)
- [OnShape Design](https://bit.ly/raspi-onshape)

The enclosure design is modulare—feel free to make your own designs and reach out to include them!

## Installation

### Prerequisites

- Raspberry Pi 2 or 3 (Pi 4 may work with modifications)
- Raspberry Pi HQ Camera
- MHS35-TFT Display (3.5" HDMI LCD)
- Battery pack for portable operation

### Setup

1. Clone the repository and navigate to the directory:
   ```bash
   git clone https://github.com/NickEngmann/piDSLM.git
   cd pidslm
   ```

2. **Configure Dropbox Access Token**:
   - Go to the [Dropbox Developers page](https://www.dropbox.com/developers/apps)
   - Create a new application
   - Generate an Access Token
   - Edit `dropbox_upload.py` and replace the placeholder token:
     ```python
     TOKEN = 'YOUR_ACCESS_TOKEN'  # Replace with your token
     ```

3. **Run the Installation Script**:
   ```bash
   sudo ./INSTALL.sh
   ```
   This will:
   - Install Python dependencies (Pillow, guizero, dropbox SDK)
   - Set up auto-start configuration
   - Configure camera settings in `/boot/config.txt`
   - Reboot the system

### Manual Installation

If you prefer manual setup:

```bash
# Install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install --upgrade Pillow

# Set up auto-start (optional)
sudo mkdir -p /home/pi/.config/autostart
sudo cp pidslm.desktop /home/pi/.config/autostart/

# Configure camera (if needed)
sudo nano /boot/config.txt
# Add: start_x=1 and gpu_mem=128
```

## Usage

### Starting the Application

Run the main application:
```bash
python3 pidslm.py
```

The application starts in fullscreen mode with the following controls:

| Button | Function |
|--------|----------|
| **Focus** | 15-second preview mode |
| **Gallery** | Browse captured photos |
| **HD 30s** | Record 30-second video |
| **Burst** | Capture up to 10,000ms of rapid photos |
| **1h 60pix** | Timelapse: 1 hour, 60-second intervals |
| **HD 30m** | Split 30-minute video into 5-second segments |
| **Upload** | Bulk upload to Dropbox |
| **Clear** | Delete all files from Downloads |

### GPIO Button Capture

The application monitors GPIO pin 16. Pressing the connected button will:
- Trigger a photo capture (3.5-second exposure)
- Save to `/home/pi/Downloads/` with timestamp filename

### Dropbox Upload

When you click the **Upload** button:
1. The app creates a busy indicator
2. `dropbox_upload.py` runs in background
3. Files in `/home/pi/Downloads/` are uploaded to Dropbox
4. Dot files, temp files, and generated files are automatically skipped

### Gallery Navigation

In gallery mode:
- Use left/right arrow buttons to navigate photos
- Thumbnails show captured `.jpg` files from Downloads folder
- Press Escape or close window to return to main menu

## File Structure

```
piDSLM/
├── pidslm.py          # Main GUI application
├── dropbox_upload.py  # Dropbox sync utility
├── INSTALL.sh         # Installation script
├── pidslm.desktop     # Auto-start configuration
├── PiDSLR.fzz         # 3D enclosure design (Fusion 360)
├── icon/              # UI icons (14 images)
└── tests/             # Test suite
    ├── test_example.py      # Example tests
    ├── conftest.py          # Test configuration with mocks
    └── embedded_mocks.py    # Hardware simulation mocks
```

## Testing

The project includes a test suite with hardware mocking:

```bash
pytest tests/ -v
```

### Test Infrastructure

- **RPi.GPIO mocked**: Simulates GPIO pin control
- **I2C/SPI/UART mocked**: Hardware communication simulation
- **guizero mocked**: GUI framework simulation
- **Source loading**: Custom fixture loads and tests actual source files

### Running Tests

Tests run successfully in both hardware and mocked environments. The mock system provides 15+ hardware module simulations for safe testing.

## Dependencies

- **Python 3.12+**
- **Pillow**: Image processing
- **guizero**: GUI framework
- **dropbox**: Dropbox API v2 SDK
- **RPi.GPIO**: Hardware control (production only)
- **raspistill/raspivid**: Camera utilities (production only)

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

## License

This project is built on the MerlinPi foundation. Please respect the original project license and any third-party dependencies.

## Support

If you found this project useful, consider supporting the design work through [PayPal](https://paypal.me/nickengman).

For questions or contributions, please reach out via the [GitHub repository](https://github.com/NickEngmann/piDSLM).

---

*Designed for Raspberry Pi enthusiasts and DIY camera projects.*
