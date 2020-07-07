from guizero import App, PushButton, Text, Window
from time import sleep
import time
import datetime
import sys, os
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

def clear():
    show_busy()
    os.system("rm -v /home/pi/Downloads/*")
    hide_busy()
    
def show_busy():
    busy.show()
    print("busy now")
    
def hide_busy():
    busy.hide()
    print("no longer busy")
    
def fullscreen():
    
    app.tk.attributes("-fullscreen", True)

def notfullscreen():
    
    app.tk.attributes("-fullscreen", False)

# Generate timestamp string generating name for photos
def timestamp():
    tstring = datetime.datetime.now()
    #print("Filename generated ...")
    return tstring.strftime("%Y%m%d_%H%M%S")

global capture_number
capture_number = timestamp()
video_capture_number = timestamp()

def burst():

    show_busy()
    capture_number = timestamp()
    print("Raspistill starts")
    os.system("raspistill -rot 90 -t 10000 -tl 0 --thumb none -n -bm -o /home/pi/Downloads/BR" +str(capture_number) + "%04d.jpg")
    print("Raspistill done")
    hide_busy()
    
def split_hd_30m():
    
    show_busy()
    capture_number = timestamp()
    print("Raspivid starts")
    os.system("raspivid -f -rot 90 -t 1800000 -sg 300000  -o /home/pi/Downloads/" +str(capture_number) + "vid%04d.h264")
    print("done")
    hide_busy()
    
#def split_slo_1h():

#def long_exp():
   
def lapse():
    
    show_busy()
    capture_number = timestamp()
    print("Raspistill timelapse starts")
    os.system("raspistill -rot 90 -t 3600000 -tl 60000 --thumb none -n -bm -o /home/pi/Downloads/TL" +str(capture_number) + "%04d.jpg")
    print("Raspistill timelapse done")
    hide_busy()

def long_preview():
    show_busy()
    print("30 second preview")
    os.system("raspistill -f -rot 90 -t 30000")
    hide_busy()

def capture_image():
    
    show_busy()
    capture_number = timestamp()
    print("Raspistill starts")
    os.system("raspistill -f -rot 90 -o /home/pi/Downloads/" +str(capture_number) + "cam.jpg")
    print("Raspistill done")
    hide_busy()

def takePicture(channel):
    print ("Button event callback")
    capture_number = timestamp()
    print("Raspistill starts")
    os.system("raspistill -f -rot 90 -t 3000 -o /home/pi/Downloads/" +str(capture_number) + "cam.jpg")
    print("Raspistill done")

def show_gallery():
    gallery = Window(app, bg="red",  height=300, width=450, title="busy")
    gallery.show()

def video_capture():
    
    show_busy()
    capture_number = timestamp()
    print("Raspivid starts")
    os.system("raspivid -f -rot 90 -t 30000 -o /home/pi/Downloads/" +str(capture_number) + "vid.h264")
    print("done")
    hide_busy()

def upload():
    
    show_busy()
    subprocess.Popen(["python3", "/home/pi/piDSLR/dropbox.py", "--yes"])
    hide_busy()
    

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.add_event_detect(16, GPIO.FALLING, callback=takePicture, bouncetime=2500)
    
app = App(layout="grid", title="Camera Controls", bg="black", width=480, height=320)

text0 = Text(app,color="white", grid=[1,0], text="- PiDSLR -")

button1 = PushButton(app, grid=[1,1], width=110, height=110, pady=35, padx=10, image="/home/pi/piDSLR/icon/prev.png", command=long_preview)
text1 = Text(app, color="white", grid=[1,2],text="Focus")
#space1 = PushButton(app, grid=[2,0], width=10, height=35, image="/home/pi/piDSLR/icon/100black.png", command=fullscreen)

button2 = PushButton(app, grid=[3,1], width=110, height=110, pady=35, padx=10, image="/home/pi/piDSLR/icon/gallery.png", command=show_gallery)
text2 = Text(app, color="white", grid=[3,2],text="Gallery")
#space2 = PushButton(app, grid=[4,0], width=10, height=10, image="/home/pi/piDSLR/icon/100black.png", command=long_preview)


button3 = PushButton(app, grid=[5,1], width=110, height=110,  pady=35, padx=10, image="/home/pi/piDSLR/icon/vid.png", command=video_capture)
text2 = Text(app, color="white", grid=[5,2],text="HD 30s")
#space3 = PushButton(app, grid=[6,0], width=10, height=10, image="/home/pi/piDSLR/icon/100black.png", command=long_preview)


button4 = PushButton(app, grid=[7,1], width=110, height=110, pady=35, padx=10, image="/home/pi/piDSLR/icon/lapse.png", command=burst)
text3 = Text(app, color="white", grid=[7,2],text="Burst")
#space4 = PushButton(app, grid=[8,0], width=10, height=10, image="/home/pi/piDSLR/icon/100black.png", command=long_preview)


button5 = PushButton(app, grid=[1,3], width=110, height=110, image="/home/pi/piDSLR/icon/self.png", command=lapse)
text4 = Text(app, color="white", grid=[1,4],text="1h 60pix")

button6 = PushButton(app, grid=[3,3], width=110, height=110, image="/home/pi/piDSLR/icon/long.png", command=split_hd_30m)
text2 = Text(app, color="white", grid=[3,4],text="HD 30m in 5s")

button7 = PushButton(app, grid=[5,3], width=110, height=110, image="/home/pi/piDSLR/icon/drop.png", command=upload)
text3 = Text(app, color="white", grid=[5,4],text="Upload")

button8 = PushButton(app, grid=[7,3], width=110, height=110, image="/home/pi/piDSLR/icon/del.png", command=clear)
text4 = Text(app, color="white", grid=[7,4],text="Clear Folder")

busy = Window(app, bg="red",  height=175, width=480, title="busy")

app.tk.attributes("-fullscreen", True)
busy.hide()
app.display()
