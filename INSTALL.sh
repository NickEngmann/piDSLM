mkdir -p /home/pi/piDSLR/icon
cp -rf icon /home/pi/piDSLR
cp dropbox_upload.py /home/pi/piDSLR/dropbox_upload.py
cp pidslr.py /home/pi/piDSLR/pidslr.py
python3 -m pip install -r requirements.txt 
