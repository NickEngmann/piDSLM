echo "Make sure paths are correct:"
mkdir -p /home/pi/piDSLR/icon
cp -rf icon /home/pi/piDSLR
cp dropbox_upload.py /home/pi/piDSLR/dropbox_upload.py
cp pidslr.py /home/pi/piDSLR/pidslr.py
echo  "Installing Pip Requirements"
python3 -m pip install -r requirements.txt
install startup.sh pidslr.py /usr/bin/
echo  "Installing piDSLR AutoStart service"
mkdir -p /home/pi/.config/autostart
install -m 644 *.desktop /home/pi/.config/autostart/
