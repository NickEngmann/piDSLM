#!/usr/bin/python3
from guizero import App, PushButton, Text, Picture, Window
from time import sleep
import time
import glob
import datetime
import sys, os
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library


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
        self.show_busy()
        capture_number = self.timestamp()
        print("Raspistill starts")
        os.system("raspistill -t 10000 -tl 0 --thumb none -n -bm -o /home/pi/Downloads/BR" +str(capture_number) + "%04d.jpg")
        print("Raspistill done")
        self.hide_busy()
        
    def split_hd_30m(self):   
        self.show_busy()
        capture_number = self.timestamp()
        print("Raspivid starts")
        os.system("raspivid -f -t 1800000 -sg 300000  -o /home/pi/Downloads/" +str(capture_number) + "vid%04d.h264")
        print("done")
        self.hide_busy()
    
    def lapse(self):
        self.show_busy()
        capture_number = self.timestamp()
        print("Raspistill timelapse starts")
        os.system("raspistill -t 3600000 -tl 60000 --thumb none -n -bm -o /home/pi/Downloads/TL" +str(capture_number) + "%04d.jpg")
        print("Raspistill timelapse done")
        self.hide_busy()

    def long_preview(self):
        self.show_busy()
        print("15 second preview")
        os.system("raspistill -f -t 15000")
        self.hide_busy()

    def capture_image(self):
        self.show_busy()
        capture_number = self.timestamp()
        print("Raspistill starts")
        os.system("raspistill -f -o /home/pi/Downloads/" +str(capture_number) + "cam.jpg")
        print("Raspistill done")
        self.hide_busy()

    def takePicture(self, channel):
        print ("Button event callback")
        capture_number = self.timestamp()
        print("Raspistill starts")
        os.system("raspistill -f -t 3500 -o /home/pi/Downloads/" +str(capture_number) + "cam.jpg")
        print("Raspistill done")

    def picture_left(self):
        if (self.picture_index == 0):
            self.pictures = (len(self.saved_pictures) - 1)    
        self.picture_index -= 1
        self.shown_picture = self.saved_pictures[self.picture_index]
        self.picture_gallery = Picture(self.gallery, width=360, height=270, image=self.shown_picture, grid=[1,0])

    def picture_right(self):
        if (self.picture_index == (len(self.saved_pictures) - 1)): 
            self.picture_index = 0 
        self.picture_index += 1
        self.shown_picture = self.saved_pictures[self.picture_index]
        self.picture_gallery = Picture(self.gallery, width=360, height=270, image=self.shown_picture, grid=[1,0])

    def show_gallery(self):
        self.gallery = Window(self.app, bg="white", height=300, width=460, layout="grid",title="Gallery")
        self.saved_pictures = glob.glob('/home/pi/Downloads/*.jpg')
        self.shown_picture = self.saved_pictures[self.picture_index] 
        button_left = PushButton(self.gallery, grid=[0,0], width=40, height=50, pady=50, padx=10, image="/home/pi/piDSLM/icon/left.png", command=self.picture_left)    
        self.picture_gallery = Picture(self.gallery, width=360, height=270, image=self.shown_picture, grid=[1,0]) 
        button_right = PushButton(self.gallery, grid=[2,0], width=40, height=50, pady=50, padx=10, image="/home/pi/piDSLM/icon/right.png", command=self.picture_right) 
        self.gallery.show()

    def video_capture(self):
        self.show_busy()
        capture_number = self.timestamp()
        print("Raspivid starts")
        os.system("raspivid -f -t 30000 -o /home/pi/Downloads/" +str(capture_number) + "vid.h264")
        print("done")
        self.hide_busy()

    def upload(self):
        self.show_busy()
        subprocess.Popen(["python3", "/home/pi/piDSLM/dropbox_upload.py", "--yes"])
        self.hide_busy()

if __name__ == '__main__':
    standalone_app = piDSLM()
    standalone_app.run()
