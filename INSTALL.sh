echo "Make sure paths are correct:"
mkdir -p /home/pi/piDSLR/icon
cp -rf icon /home/pi/piDSLR
cp dropbox_upload.py /home/pi/piDSLR/dropbox_upload.py
cp pidslr.py /home/pi/piDSLR/pidslr.py
echo  "Installing Pip Requirements"
python3 -m pip install -r requirements.txt
install pidslr.py /usr/bin/
echo  "Installing piDSLR AutoStart service"
mkdir -p /home/pi/.config/autostart
install -m 644 *.desktop /home/pi/.config/autostart/
sed -i -e '$i \start_x=1\ngpu_mem=128\n' /boot/config.txt
echo "Installation Finished, Rebooting Now"
sleep 2
reboot now
