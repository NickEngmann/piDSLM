piDSLM - Raspberry Pi Digital Single Lens Mirrorless
===============

Camera project for Raspberry Pi 2/3 + HQ Camera + MHS35-TFT

<img src="https://i.imgur.com/VspFA5V.jpg" data-canonical-src="https://i.imgur.com/VspFA5V.jpg" width="400" height="400" />

# Introduction

A standalone battery-powered DSLR interface for the Raspberry Pi HQ Camera, featuring GPIO controls, on-device gallery display, and cloud backup via Dropbox.

## Design Features

### Enclosure Improvements

The piDSLM enclosure is designed for modularity and ease of use:

- **Modular Design**: Interchangeable camera grips and mounting options
- **3D Printable**: Entire enclosure designed for FDM printing
- **Compact Form Factor**: Optimized for portability while maintaining accessibility
- **Heat Management**: Ventilation channels for extended operation

### Design Files

- **CAD Source**: [PiDSLR.fzz](PiDSLR.fzz) - FreeCAD/OpenSCAD design file
- **OnShape**: [View on OnShape](https://bit.ly/raspi-onshape) - Interactive 3D model
- **Export Formats**: 
  - STL files available for 3D printing
  - STEP files for CAD modifications

### Modular Grips

The design supports interchangeable grips for different use cases:
- Standard vertical grip
- Horizontal orientation grip
- Tripod mount adapter

*Feel free to create your own grip designs and contribute!*

For More Info:

<<<<<<< Updated upstream
- [Hackster](https://www.hackster.io/projects/2a86c3)
- [GitHub](https://github.com/NickEngmann/piDSLM)
- [Instructables] ( TBD )

Designed using
- [OnShape](https://bit.ly/raspi-onshape)

If you found this useful, please donate what you think it is worth to my [paypal.me](https://paypal.me/nickengman). Help cover the time of design.
=======
- [Hackster Project Page](https://www.hackster.io/projects/2a86c3)
- [GitHub Repository](https://github.com/NickEngmann/piDSLM)
- [OnShape Design (Interactive 3D Model)](https://bit.ly/raspi-onshape)

## Support

This project is part of an open-source hardware and software initiative. If you found it useful:
>>>>>>> Stashed changes

- Star the repository to show support
- [PayPal](https://paypal.me/nickengman) - Contribute to design and development time
- Share your modifications and improvements!

---

# Technical Overview

## Hardware Requirements

- Raspberry Pi 2/3/4
- Raspberry Pi HQ Camera or Camera Module v2
- MHS35-TFT Display (3.5" LCD)
- GPIO Button for shutter control
- Optional: Battery pack for portable operation

## Software Features

- **Photo Capture**: Still images via `raspistill`
- **Video Recording**: HD video via `raspivid`
- **Burst Mode**: 10-second burst capture
- **Timelapse**: 1-hour timelapse (60-second intervals)
- **Gallery View**: On-device image browser
- **Dropbox Sync**: Automatic cloud backup

## Design Tools

- **CAD**: OnShape (cloud-based) and FreeCAD
- **3D Printing**: FDM compatible designs
- **GUI Framework**: guizero (Python)
- **Hardware Interface**: RPi.GPIO

---

# Installation

<<<<<<< Updated upstream
For the codebase, I built the piDSLM codebase off of a forked a copy of fellow DIYer Martin Manders [MerlinPi project](https://github.com/MisterEmm/MerlinPi). The piDSLM codebase is still in its infancy but it allows the user to take photos/videos, and view them in a gallery. It also allows users to bulk upload the footage to Dropbox. To begin ssh into the Raspberry Pi and run the following command:

```

=======
## Hardware Assembly

1. Print enclosure parts using the provided STL files
2. Assemble Raspberry Pi, display, and camera module
3. Connect GPIO button to pin 16 (BCM)
4. Power on and verify all connections

## Software Setup

piDSLM builds upon Martin Manders' [MerlinPi project](https://github.com/MisterEmm/MerlinPi). While still in active development, it provides:
- Photo/video capture
- On-device gallery viewing
- Dropbox cloud upload

### Prerequisites

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-rpi.gpio python3-guizero
sudo apt-get install -y libfreetype6-dev libffi-dev
```

### Installation Steps

1. Clone the repository:
```bash
>>>>>>> Stashed changes
git clone https://github.com/NickEngmann/pidslm.git
cd pidslm
```

<<<<<<< Updated upstream
You're then going to retrieve a Dropbox Access token to enable to Dropbox footage upload feature. To do this go ahead and [go to the Application Developer page on Dropbox](https://www.dropbox.com/developers/apps). Create an application and click the Generate Access Token button to generate your access token.

Then replace the dummy access token in Dropbox_upload.py with your new access token.

```

# OAuth2 access token.  TODO: login etc.
TOKEN = 'YOUR_ACCESS_TOKEN'
```

Finally, run the INSTALL.sh script using the following command

```
=======
2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Configure Dropbox (optional - for cloud sync):
   - Go to [Dropbox Developer Apps](https://www.dropbox.com/developers/apps)
   - Create an application
   - Generate an Access Token
   - Edit `dropbox_upload.py` and replace the token:

```python
# OAuth2 access token
TOKEN = 'YOUR_ACTUAL_DROPBOX_ACCESS_TOKEN'
```

4. Run the installer:
```bash
>>>>>>> Stashed changes
sudo ./INSTALL.sh
```

5. Launch the application:
```bash
python3 pidslm.py
```

### Desktop Auto-Start

The application is configured to auto-launch via the [pidslm.desktop](pidslm.desktop) file for seamless operation on boot.

---

# File Structure

```
piDSLM/
├── pidslm.py          # Main GUI application
├── dropbox_upload.py  # Dropbox sync utility
├── PiDSLR.fzz         # 3D enclosure design file
├── DESIGN_IMPROVEMENTS.md  # Design improvement documentation
├── 3D_PRINTING_GUIDE.md    # 3D printing instructions
├── icon/              # GUI icons and images
├── INSTALL.sh         # Installation script
├── README.md          # This file
└── tests/             # Test suite
```

---

# License

This project is open-source hardware and software. Feel free to modify, share, and build upon it. Attribution appreciated but not required.

## Design License

The enclosure design is released under Creative Commons Attribution-ShareAlike 4.0 International License. See [DESIGN_IMPROVEMENTS.md](DESIGN_IMPROVEMENTS.md) for details.



