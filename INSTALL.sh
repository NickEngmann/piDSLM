echo "Make sure paths are correct:"
mkdir -p /home/pi/piDSLM/icon
cp -rf icon /home/pi/piDSLM
cp dropbox_upload.py /home/pi/piDSLM/dropbox_upload.py
cp pidslm.py /home/pi/piDSLM/pidslm.py
echo  "Installing Pip Requirements"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install --upgrade Pillow
echo  "Installing piDSLM AutoStart service"
sudo install pidslm.py /usr/bin/
sudo mkdir -p /home/pi/.config/autostart
sudo install -m 644 *.desktop /home/pi/.config/autostart/
sudo sed -i -e '$i \start_x=1\ngpu_mem=128\n' /boot/config.txt
echo "Installation Finished, Rebooting Now"
sleep 2
reboot now
