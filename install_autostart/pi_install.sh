#!/bin/bash

apt-get update && apt-get upgrade -y

sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y

cd /home/admin/

mkdir Programs

cd Programs

mkdir Pi_Photo_Stand

cd /home/admin/

mkdir TE_NAS_photo_share

pip3 install opencv-python==4.5.3.56

pip3 install numpy==1.21.2

pip3 install pyautogui

sudo apt install cifs-utils -y

# Check if /boot/config.txt exists
# Add config for 5 inch display
if [ -f /boot/config.txt ]; then
    # Append the line to /boot/config.txt
    echo "hdmi_group=2" | sudo tee -a /boot/config.txt > /dev/null
    echo "hdmi_mode=87" | sudo tee -a /boot/config.txt > /dev/null
    echo "hdmi_cvt 800 480 60 6 0 0 0" | sudo tee -a /boot/config.txt > /dev/null
    echo "hdmi_drive=1" | sudo tee -a /boot/config.txt > /dev/null
    echo "Line 'hdmi_group=2' added to /boot/config.txt"
else
    echo "/boot/config.txt not found. Please check your system configuration."
fi

# Line to be added
new_line="//192.168.178.27/Global-Share/pi_photo_stand /home/admin/TE_NAS_photo_share cifs user,username=Niklas,password=,vers=3.0 0 0"

# Check if /etc/fstab exists
if [ -f /etc/fstab ]; then
    # Append the line to /etc/fstab
    echo "$new_line" | sudo tee -a /etc/fstab > /dev/null
    echo "Line added to /etc/fstab"
else
    echo "/etc/fstab not found. Please check your system configuration."
fi

#sudo nano /etc/fstab

cd /home/admin/Programs/Pi_Photo_Stand/

git clone https://github.com/NiklasTry/pi_photo_stand.git

sudo cp install_autostart/autostart_pi_stand.service /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable autostart_pi_stand

sudo systemctl start autostart_pi_stand

sudo systemctl status autostart_pi_stand

sleep 10


