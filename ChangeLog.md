Changes to adafruit-pi-cam
==========================

Version 2.1 (Direct Quit)
-------------------------

- **new feature**: after boot, the first setting screen is the
                   quit confirmation page. This allows faster shutdown.
- **internal**:    code changes for future enhancements


Version 2 (major rework)
------------------------

This version needs a newer version of python-picam (tested with
version 1.8). It additionally needs the package python-pyexiv2.

- **new feature**: added screen for setting AWB
- **new feature**: add thumbnail to captured image and save to /home/pi/.cache
- **performance**: display cached thumbnails instead of scaled down images
- **performance**: keep list of images-numbers instead of testing existence
                   of files with thousands of os-calls
- **change**:      name images rpi_XXXX.jpg instead of IMG_XXXX.JPG
                   (unix-tools usually expect lower case in filenames)
- **fix**:         change owner of captured images to pi:pi
- **fix**:         capture raw RGB directly, no need to scale result with C-code
- **fix**:         removed buggy cropping code (camera.crop is deprecated)
- **fix**:         added shebang (no need to call python explicitly to execute code)
- **fix**:         start cam.py from any directory
                   (in *nix, you should stay at HOME)
- **fix**:         read and write cam.pkl in user's HOME-directory
- **new feature**: set EXIF-tag 'WhiteBalance' to auto or manual


Version 1 (original Adafruit release)
-------------------------------------

