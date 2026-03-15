#!/usr/bin/python3
from guizero import App, PushButton, Text, Picture, Window
from time import sleep
import time
import glob
import datetime
import sys, os
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from capture import ImageCapture, GalleryManager, CaptureResult


class piDSLM:
    def __init__(self):
        self.capture_number = self.timestamp()
        self.video_capture_number = self.timestamp()
        self.picture_index = 0
        self.saved_pictures = []
        self.shown_picture = ""

        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(16, GPIO.FALLING, callback=self.takePicture, bouncetime=2500)

        # Initialize capture manager with real hardware support
        self.capture_manager = ImageCapture(
            output_dir='/home/pi/Downloads',
            capture_command='raspistill',
            is_hardware_available=True
        )
        
        # Initialize gallery manager
        self.gallery_manager = GalleryManager(photo_dir='/home/pi/Downloads')

        self.app = App(layout="grid", title="Camera Controls", bg="black", width=480, height=320)

        text0 = Text(self.app,color="white", grid=[1,0], text="- PiDSLM -")

        button1 = PushButton(self.app, grid=[1,1], width=110, height=110, pady=35, padx=10, image="/home/pi/piDSLM/icon/prev.png", command=self.long_preview)
        text1 = Text(self.app, color="white", grid=[1,2],text="Focus")

        button2 = PushButton(self.app, grid=[3,1], width=110, height=110, pady=35, padx=10, image="/home/pi/piDSLM/icon/gallery.png", command=self.show_gallery)
        text2 = Text(self.app, color="white", grid=[3,2],text="Gallery")

        button3 = PushButton(self.app, grid=[5,1], width=110, height=110,  pady=35, padx=10, image="/home/pi/piDSLM/icon/vid.png", command=self.video_capture)
        text2 = Text(self.app, color="white", grid=[5,2],text="HD 30s")

        button4 = PushButton(self.app, grid=[7,1], width=110, height=110, pady=35, padx=10, image="/home/pi/piDSLM/icon/lapse.png", command=self.burst)
        text3 = Text(self.app, color="white", grid=[7,2],text="Burst")

        button5 = PushButton(self.app, grid=[1,3], width=110, height=110, image="/home/pi/piDSLM/icon/self.png", command=self.lapse)
        text4 = Text(self.app, color="white", grid=[1,4],text="1h 60pix")

        button6 = PushButton(self.app, grid=[3,3], width=110, height=110, image="/home/pi/piDSLM/icon/long.png", command=self.split_hd_30m)
        text2 = Text(self.app, color="white", grid=[3,4],text="HD 30m in 5s")

        button7 = PushButton(self.app, grid=[5,3], width=110, height=110, image="/home/pi/piDSLM/icon/drop.png", command=self.upload)
        text3 = Text(self.app, color="white", grid=[5,4],text="Upload")

        button8 = PushButton(self.app, grid=[7,3], width=110, height=110, image="/home/pi/piDSLM/icon/del.png", command=self.clear)
        text4 = Text(self.app, color="white", grid=[7,4],text="Clear Folder")

        self.busy = Window(self.app, bg="red",  height=175, width=480, title="busy")

        self.app.tk.attributes("-fullscreen", True)
        self.busy.hide()
        self.app.display()

    def clear(self):
        self.show_busy()
        os.system("rm -v /home/pi/Downloads/*")
        self.hide_busy()
    
    def show_busy(self):
        self.busy.show()
        print("busy now")
        
    def hide_busy(self):
        self.busy.hide()
        print("no longer busy")
        
    def fullscreen(self):
        self.app.tk.attributes("-fullscreen", True)

    def notfullscreen(self):
        self.app.tk.attributes("-fullscreen", False)

    # Generate timestamp string generating name for photos
    def timestamp(self):
        tstring = datetime.datetime.now()
        #print("Filename generated ...")
        return tstring.strftime("%Y%m%d_%H%M%S")
  
    def burst(self):
        """Capture burst photos using the capture manager."""
        self.show_busy()
        result = self.capture_manager.burst_capture(
            prefix="BR",
            timeout_ms=10000,
            interval_ms=0
        )
        if result.success:
            print(f"Burst capture saved to: {result.filepath}")
        else:
            print(f"Burst capture failed: {result.error}")
        self.hide_busy()
        
    def split_hd_30m(self):
        """Record 30m video split into 5s segments using the capture manager."""
        self.show_busy()
        result = self.capture_manager.video_capture(
            prefix="vid",
            timeout_ms=1800000,  # 30 minutes
            is_frame_sequence=True,
            segment_time_ms=5000  # 5 second segments
        )
        if result.success:
            print(f"Video capture saved to: {result.filepath}")
        else:
            print(f"Video capture failed: {result.error}")
        self.hide_busy()
    
    def lapse(self):
        """Capture timelapse sequence using the capture manager."""
        self.show_busy()
        result = self.capture_manager.timelapse(
            prefix="TL",
            timeout_ms=3600000,  # 1 hour
            interval_ms=60000  # 60 seconds between captures
        )
        if result.success:
            print(f"Timelapse capture saved to: {result.filepath}")
        else:
            print(f"Timelapse capture failed: {result.error}")
        self.hide_busy()

    def long_preview(self):
        """Show 15-second preview using the capture manager."""
        self.show_busy()
        result = self.capture_manager.capture(
            prefix="preview_",
            timeout_ms=15000,
            is_live=True
        )
        self.hide_busy()

    def capture_image(self):
        """Capture a single image using the capture manager."""
        self.show_busy()
        result = self.capture_manager.capture(
            prefix="cam",
            timeout_ms=3500,
            extension=".jpg"
        )
        if result.success:
            print(f"Image captured: {result.filepath}")
        else:
            print(f"Capture failed: {result.error}")
        self.hide_busy()

    def takePicture(self, channel):
        """Callback for GPIO button press - capture image using the capture manager."""
        print("Button event callback")
        result = self.capture_manager.capture(
            prefix="cam",
            timeout_ms=3500,
            extension=".jpg"
        )
        if result.success:
            print(f"Image captured: {result.filepath}")
        else:
            print(f"Capture failed: {result.error}")

    def picture_left(self):
        """Navigate to previous photo in gallery."""
        if self.picture_index == 0:
            self.picture_index = len(self.saved_pictures) - 1
        self.picture_index -= 1
        self.shown_picture = self.saved_pictures[self.picture_index]
        self.picture_gallery = Picture(self.gallery, width=360, height=270, 
                                       image=self.shown_picture, grid=[1,0])

    def picture_right(self):
        """Navigate to next photo in gallery."""
        if self.picture_index == (len(self.saved_pictures) - 1):
            self.picture_index = 0
        self.picture_index += 1
        self.shown_picture = self.saved_pictures[self.picture_index]
        self.picture_gallery = Picture(self.gallery, width=360, height=270,
                                       image=self.shown_picture, grid=[1,0])

    def show_gallery(self):
        """Display photo gallery using GalleryManager."""
        self.gallery = Window(self.app, bg="white", height=300, width=460, 
                             layout="grid", title="Gallery")
        
        # Load photos from directory
        self.saved_pictures = self.gallery_manager.load_photos()
        
        if not self.saved_pictures:
            Text(self.gallery, text="No photos found", grid=[1, 0])
            return
        
        self.picture_index = 0
        self.shown_picture = self.saved_pictures[self.picture_index]
        
        button_left = PushButton(self.gallery, grid=[0,0], width=40, height=50, 
                                 pady=50, padx=10, 
                                 image="/home/pi/piDSLM/icon/left.png",
                                 command=self.picture_left)
        self.picture_gallery = Picture(self.gallery, width=360, height=270, 
                                       image=self.shown_picture, grid=[1,0])
        button_right = PushButton(self.gallery, grid=[2,0], width=40, height=50, 
                                  pady=50, padx=10, 
                                  image="/home/pi/piDSLM/icon/right.png",
                                  command=self.picture_right)
        self.gallery.show()

    def video_capture(self):
        """Capture video using the capture manager."""
        self.show_busy()
        result = self.capture_manager.video_capture(
            prefix="vid",
            timeout_ms=30000,  # 30 seconds
            is_frame_sequence=False
        )
        if result.success:
            print(f"Video captured: {result.filepath}")
        else:
            print(f"Video capture failed: {result.error}")
        self.hide_busy()

    def upload(self):
        self.show_busy()
        subprocess.Popen(["python3", "/home/pi/piDSLM/dropbox_upload.py", "--yes"])
        self.hide_busy()

if __name__ == '__main__':
    standalone_app = piDSLM()
    standalone_app.run()
