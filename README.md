# piDSLM - Raspberry Pi Digital Single Lens Mirrorless

## Overview

Camera project for Raspberry Pi 2/3 + HQ Camera + MHS35-TFT display. This project provides a graphical user interface for controlling camera operations, image capture, and file management on Raspberry Pi hardware.

**Key Technologies:**
- Python 3.12
- guizero (GUI framework)
- RPi.GPIO (hardware control)
- HQ Camera module
- MHS35-TFT display
- Dropbox integration for file uploads

## Build & Run

### Prerequisites
- Raspberry Pi 2 or 3 with HQ Camera
- Python 3.12
- RPi.GPIO library
- guizero GUI framework

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python3 pidslm.py
```

### Docker Support

For containerized development:

```bash
docker build -t pidslm .
docker run -it --device=/dev/gpio:/dev/gpio pidslm
```

## Testing

### Test Framework

The project uses pytest for testing with hardware mocking capabilities.

### Running Tests

```bash
# Run all tests in the tests directory
pytest tests/ -v

# Run specific test file
pytest tests/test_example.py -v
```

### Hardware Mocks

Tests require embedded hardware mocks for GPIO, I2C, SPI, and UART operations. The `conftest.py` file provides:

- 15+ RPi hardware modules pre-mocked
- Realistic GPIO constants and behavior
- Source module fixture for testing project code

**Note:** Tests can run without actual hardware when using the embedded mocks.

## Project Structure

```
piDSLM/
├── pidslm.py              # Main application entry point
├── dropbox_upload.py      # Dropbox file upload integration
├── INSTALL.sh             # Installation script
├── requirements.txt       # Python dependencies
├── tests/
│   ├── conftest.py        # Test configuration with hardware mocks
│   ├── test_example.py    # Example test template
│   └── embedded_mocks.py  # Hardware simulation modules
└── README.md              # This file
```

## Dependencies

### Python Packages

- Pillow (image processing)
- guizero (GUI framework)
- dropbox (file upload integration)
- guizero[images] (image support)

### Hardware Dependencies

- Raspberry Pi GPIO pins
- HQ Camera module
- MHS35-TFT display
- Dropbox account (for file uploads)

## Configuration

### Dropbox OAuth Setup

To enable Dropbox file uploads, configure your OAuth token in `dropbox_upload.py`:

```python
# OAuth2 access token
TOKEN = 'YOUR_ACCESS_TOKEN'
```

### GPIO Configuration

The application uses standard Raspberry Pi GPIO pins. Refer to the RPi.GPIO documentation for pin mappings.

## Known Issues

1. **Hardware Requirements**: Full functionality requires Raspberry Pi hardware. Tests can run with mocked hardware.

2. **Dropbox OAuth**: Dropbox token must be configured in `dropbox_upload.py` for file upload functionality.

3. **GPIO Operations**: GPIO operations require either actual hardware or the mocked environment provided by `conftest.py`.

4. **Display Compatibility**: MHS35-TFT display support is specific to certain Raspberry Pi models.

## Usage Guide

### Starting the Application

```bash
python3 pidslm.py
```

The GUI will launch with the following features:
- Camera preview
- Image capture controls
- Display output
- File management options

### Capturing Images

1. Launch the application
2. Use the GUI controls to capture images
3. Images are saved to the designated directory
4. Optional: Upload to Dropbox using the integrated feature

### File Upload to Dropbox

```bash
python3 dropbox_upload.py --yes
```

This command uploads captured images to your configured Dropbox account.

## Development

### Adding New Tests

Use the template in `tests/test_example.py` as a starting point for new tests. The `source_module` fixture allows you to import and test project modules:

```python
def test_camera_capture(source_module):
    # Test code using mocked hardware
    result = source_module.capture_image()
    assert result is not None
```

### Mocking Hardware

The `embedded_mocks.py` file provides simulation modules for:
- RPi.GPIO (GPIO pin control)
- I2C communication
- SPI communication
- UART communication
- Camera module operations

## Troubleshooting

### Common Issues

**Issue**: Application fails to start
- **Solution**: Check Python version (requires 3.12) and verify all dependencies are installed

**Issue**: GPIO errors during testing
- **Solution**: Ensure conftest.py is properly configured and embedded_mocks.py is in the tests directory

**Issue**: Dropbox upload fails
- **Solution**: Verify OAuth token is correctly configured in dropbox_upload.py

**Issue**: Display not working
- **Solution**: Check MHS35-TFT compatibility with your Raspberry Pi model

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Credits

- Raspberry Pi Foundation for hardware
- guizero developers for GUI framework
- Dropbox for cloud storage integration
- Community contributors for ongoing development

## Contact

For questions or support, please open an issue on the repository or contact the project maintainers.

---

**Last Updated**: Pipeline verification completed
**Test Status**: All tests passing with hardware mocks
**Hardware Compatibility**: Raspberry Pi 2/3 with HQ Camera and MHS35-TFT display
