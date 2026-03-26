#!/usr/bin/python3
"""piDSLM - Raspberry Pi Digital Single Lens Mirrorless Camera Interface.

Main application providing GUI controls for camera capture, gallery viewing,
video recording, and Dropbox integration.
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from guizero import App, PushButton, Text, Picture, Window
import RPi.GPIO as GPIO

# Import configuration module
from config import PiDSLMConfig, get_config

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


class piDSLM:
    """Main piDSLM application class."""

    def __init__(self, config: Optional[PiDSLMConfig] = None):
        """Initialize the piDSLM application.

        Args:
            config: Optional configuration instance. If not provided,
                   uses get_config() to load default or environment config.
        """
        self.config = config or get_config()
        self.capture_number: Optional[str] = None
        self.video_capture_number: Optional[str] = None
        self.picture_index = 0
        self.saved_pictures: list[str] = []
        self.shown_picture: str = ""
        self.gallery: Optional[Window] = None
        self.busy: Optional[Window] = None
        self.app: Optional[App] = None

        # Setup GPIO for button control
        self._setup_gpio()

        # Initialize GUI
        self._init_gui()

        logger.info("piDSLM application initialized successfully")
        logger.debug(f"Downloads directory: {self.config.downloads_dir}")
        logger.debug(f"Icon directory: {self.config.icon_dir}")

    def _setup_gpio(self) -> None:
        """Setup GPIO for physical button control."""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(
            self.config.button_pin,
            GPIO.IN,
            pull_up_down=GPIO.PUD_UP
        )
        GPIO.add_event_detect(
            self.config.button_pin,
            GPIO.FALLING,
            callback=self.takePicture,
            bouncetime=self.config.button_bounce_time
        )
        logger.info(f"GPIO button setup complete on pin {self.config.button_pin}")

    def _init_gui(self) -> None:
        """Initialize the GUI application."""
        self.app = App(
            layout="grid",
            title="Camera Controls",
            bg="black",
            width=480,
            height=320
        )

        # Title text
        text0 = Text(self.app, color="white", grid=[1, 0], text="- PiDSLM -")

        # Setup icon paths using config
        icon_dir = self.config.icon_dir
        prev_icon = os.path.join(icon_dir, "prev.png")
        gallery_icon = os.path.join(icon_dir, "gallery.png")
        vid_icon = os.path.join(icon_dir, "vid.png")
        lapse_icon = os.path.join(icon_dir, "lapse.png")
        self_icon = os.path.join(icon_dir, "self.png")
        long_icon = os.path.join(icon_dir, "long.png")
        drop_icon = os.path.join(icon_dir, "drop.png")
        del_icon = os.path.join(icon_dir, "del.png")
        left_icon = os.path.join(icon_dir, "left.png")
        right_icon = os.path.join(icon_dir, "right.png")

        # Camera control buttons
        button1 = PushButton(
            self.app, grid=[1, 1], width=110, height=110, pady=35, padx=10,
            image=prev_icon, command=self.long_preview
        )
        Text(self.app, color="white", grid=[1, 2], text="Focus")

        button2 = PushButton(
            self.app, grid=[3, 1], width=110, height=110, pady=35, padx=10,
            image=gallery_icon, command=self.show_gallery
        )
        Text(self.app, color="white", grid=[3, 2], text="Gallery")

        button3 = PushButton(
            self.app, grid=[5, 1], width=110, height=110, pady=35, padx=10,
            image=vid_icon, command=self.video_capture
        )
        Text(self.app, color="white", grid=[5, 2], text="HD 30s")

        button4 = PushButton(
            self.app, grid=[7, 1], width=110, height=110, pady=35, padx=10,
            image=lapse_icon, command=self.burst
        )
        Text(self.app, color="white", grid=[7, 2], text="Burst")

        button5 = PushButton(
            self.app, grid=[1, 3], width=110, height=110,
            image=self_icon, command=self.lapse
        )
        Text(self.app, color="white", grid=[1, 4], text="1h 60pix")

        button6 = PushButton(
            self.app, grid=[3, 3], width=110, height=110, pady=35, padx=10,
            image=long_icon, command=self.split_hd_30m
        )
        Text(self.app, color="white", grid=[3, 4], text="HD 30m in 5s")

        button7 = PushButton(
            self.app, grid=[5, 3], width=110, height=110, pady=35, padx=10,
            image=drop_icon, command=self.upload
        )
        Text(self.app, color="white", grid=[5, 4], text="Upload")

        button8 = PushButton(
            self.app, grid=[7, 3], width=110, height=110, pady=35, padx=10,
            image=del_icon, command=self.clear
        )
        Text(self.app, color="white", grid=[7, 4], text="Clear Folder")

        # Busy window
        self.busy = Window(self.app, bg="red", height=175, width=480, title="busy")

        # Setup fullscreen and display
        self.app.tk.attributes("-fullscreen", True)
        self.busy.hide()
        self.app.display()

        logger.info("GUI initialization complete")

    def _get_capture_command(self, output_pattern: str) -> str:
        """Get capture command with timestamp.

        Args:
            output_pattern: Pattern for output file with timestamp placeholder

        Returns:
            Full command string with timestamp
        """
        capture_number = self.timestamp()
        return output_pattern % capture_number

    def show_busy(self) -> None:
        """Show busy indicator window."""
        if self.busy:
            self.busy.show()
            logger.debug("Busy window shown")

    def hide_busy(self) -> None:
        """Hide busy indicator window."""
        if self.busy:
            self.busy.hide()
            logger.debug("Busy window hidden")

    def timestamp(self) -> str:
        """Generate timestamp string for filename.

        Returns:
            Timestamp string in format YYYYMMDD_HHMMSS
        """
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def burst(self) -> None:
        """Capture burst mode photos (10000ms duration, 0ms interval)."""
        self.show_busy()
        output_path = self.config.get_capture_output_path("BR%s%%04d.jpg")
        cmd = f"raspistill -t 10000 -tl 0 --thumb none -n -bm -o {output_path}"
        logger.info(f"Burst mode command: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                logger.info("Burst capture completed successfully")
            else:
                logger.error(f"Burst capture failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error("Burst capture timed out")
        finally:
            self.hide_busy()

    def split_hd_30m(self) -> None:
        """Record 30-minute video in 5-second segments."""
        self.show_busy()
        output_path = self.config.get_capture_output_path("%svid%%04d.h264")
        cmd = f"raspivid -f -t 1800000 -sg 300000 -o {output_path}"
        logger.info(f"Split HD 30m command: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=2000)
            if result.returncode == 0:
                logger.info("Split HD 30m capture completed successfully")
            else:
                logger.error(f"Split HD 30m capture failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error("Split HD 30m capture timed out")
        finally:
            self.hide_busy()

    def lapse(self) -> None:
        """Capture timelapse photos (1 hour duration, 60 second intervals)."""
        self.show_busy()
        output_path = self.config.get_capture_output_path("TL%s%%04d.jpg")
        cmd = f"raspistill -t 3600000 -tl 60000 --thumb none -n -bm -o {output_path}"
        logger.info(f"Timelapse command: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3700)
            if result.returncode == 0:
                logger.info("Timelapse capture completed successfully")
            else:
                logger.error(f"Timelapse capture failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error("Timelapse capture timed out")
        finally:
            self.hide_busy()

    def long_preview(self) -> None:
        """Show 15-second live preview for focusing."""
        self.show_busy()
        cmd = "raspistill -f -t 15000"
        logger.info(f"Long preview command: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
            if result.returncode == 0:
                logger.info("Long preview completed")
            else:
                logger.error(f"Long preview failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error("Long preview timed out")
        finally:
            self.hide_busy()

    def capture_image(self) -> None:
        """Capture a single photo with preview."""
        self.show_busy()
        output_path = self.config.get_capture_output_path("%scam.jpg")
        cmd = f"raspistill -f -o {output_path}"
        logger.info(f"Capture image command: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logger.info("Image capture completed successfully")
            else:
                logger.error(f"Image capture failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error("Image capture timed out")
        finally:
            self.hide_busy()

    def takePicture(self, channel: Optional[int] = None) -> None:
        """Callback for GPIO button press - capture a photo."""
        logger.info("Button event triggered")
        output_path = self.config.get_capture_output_path("%scam.jpg")
        cmd = f"raspistill -f -t 3500 -o {output_path}"
        logger.info(f"Photo capture command: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logger.info("Photo capture completed successfully")
            else:
                logger.error(f"Photo capture failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error("Photo capture timed out")

    def picture_left(self) -> None:
        """Navigate to previous picture in gallery."""
        if self.picture_index == 0 and len(self.saved_pictures) > 1:
            self.picture_index = len(self.saved_pictures) - 1
        elif self.picture_index > 0:
            self.picture_index -= 1
        self._display_current_picture()

    def picture_right(self) -> None:
        """Navigate to next picture in gallery."""
        if self.picture_index < len(self.saved_pictures) - 1:
            self.picture_index += 1
        elif self.picture_index == len(self.saved_pictures) - 1:
            self.picture_index = 0
        self._display_current_picture()

    def _display_current_picture(self) -> None:
        """Display the current picture in the gallery."""
        if self.gallery and self.saved_pictures and self.picture_index < len(self.saved_pictures):
            self.shown_picture = self.saved_pictures[self.picture_index]
            # Clear any existing picture widget
            for widget in self.gallery.children:
                if isinstance(widget, Picture):
                    widget.destroy()
            # Display new picture
            Picture(
                self.gallery,
                width=360,
                height=270,
                image=self.shown_picture,
                grid=[1, 0]
            )
            logger.debug(f"Displayed picture: {self.shown_picture}")

    def show_gallery(self) -> None:
        """Show gallery of captured photos."""
        logger.info("Opening gallery")
        self.gallery = Window(
            self.app,
            bg="white",
            height=300,
            width=460,
            layout="grid",
            title="Gallery"
        )

        # Find all jpg files in downloads directory
        download_path = Path(self.config.downloads_dir)
        self.saved_pictures = sorted([
            str(p) for p in download_path.glob("*.jpg")
        ])

        logger.info(f"Found {len(self.saved_pictures)} photos in gallery")

        if not self.saved_pictures:
            Text(
                self.gallery,
                color="black",
                grid=[1, 0],
                text="No photos found"
            )
            return

        self.picture_index = 0
        self.shown_picture = self.saved_pictures[0]
        self._display_current_picture()

        # Setup navigation buttons
        icon_dir = self.config.icon_dir
        left_icon = os.path.join(icon_dir, "left.png")
        right_icon = os.path.join(icon_dir, "right.png")

        PushButton(
            self.gallery,
            width=40,
            height=50,
            pady=50,
            padx=10,
            image=left_icon,
            command=self.picture_left,
            grid=[0, 0]
        )

        PushButton(
            self.gallery,
            width=40,
            height=50,
            pady=50,
            padx=10,
            image=right_icon,
            command=self.picture_right,
            grid=[2, 0]
        )

        self.gallery.show()

    def upload(self) -> None:
        """Upload files to Dropbox."""
        self.show_busy()
        logger.info("Starting Dropbox upload")

        # Build upload command
        upload_script = os.path.join(self.config.home_dir, "piDSLM", "dropbox_upload.py")
        cmd = [sys.executable, upload_script, "--yes"]

        # Use environment from config if Dropbox is enabled
        env = os.environ.copy()
        if self.config.dropbox_token:
            env["DROPBOX_ACCESS_TOKEN"] = self.config.dropbox_token

        logger.info(f"Running upload command: {' '.join(cmd)}")
        subprocess.Popen(cmd, env=env)
        logger.info("Upload process started")

        self.hide_busy()

    def clear(self) -> None:
        """Clear all files from the downloads directory."""
        self.show_busy()
        logger.info(f"Clearing files from: {self.config.downloads_dir}")

        try:
            download_path = Path(self.config.downloads_dir)
            files = list(download_path.glob("*"))
            cleared = 0
            for f in files:
                try:
                    if f.is_file():
                        f.unlink()
                        cleared += 1
                except OSError as e:
                    logger.warning(f"Could not delete {f}: {e}")

            logger.info(f"Cleared {cleared} files from downloads directory")
        except Exception as e:
            logger.error(f"Failed to clear directory: {e}")
        finally:
            self.hide_busy()

    def cleanup(self) -> None:
        """Clean up GPIO and resources."""
        logger.info("Cleaning up resources")
        GPIO.cleanup()
        if self.app:
            self.app.destroy()


if __name__ == '__main__':
    # Create and run application
    standalone_app = piDSLM()
    try:
        standalone_app.run()
    except KeyboardInterrupt:
        logger.info("Application interrupted")
    finally:
        standalone_app.cleanup()
