SIZE_VIRTUAL_MEMORY=50000 # Mbyte

echo "### Cleaning the OS installation"
sudo apt-get clean
sudo apt-get autoremove -y

echo "### Installing dependencies for automatic USB management"
sudo apt-get install python3-pip -y
sudo pip3 install watchdog
sudo pip3 install datetime

echo "### Creating folder for logs (available only for pi user)"
sudo mkdir /home/pi/Documents/
sudo mkdir /home/pi/Documents/logs
sudo mkdir /home/pi/Documents/logs/usb_share

echo "### Adding dwc2 to startup kernel modules"
echo "dwc2" >> /etc/modules

echo "### Enabling USB driver"
echo "dtoverlay=dwc2,dr_mode=peripheral" >> /boot/config.txt

echo "### Allocating virtual memory"
sudo dd bs=1M if=/dev/zero of=/piusb.bin count=$SIZE_VIRTUAL_MEMORY

echo "### Formatting virtual memory"
sudo mkdosfs /piusb.bin -F 32 -I

echo "### Creation of folders where to mount the virtual drive"
sudo mkdir /mnt/usb_share

echo "### Add virtual drive to known disk partitions"
echo "/piusb.bin /mnt/usb_share vfat users,umask=000 0 2" >> /etc/fstab

echo "### Installation of service for automatic USB management"
sudo cp usb_share.py /usr/local/share
sudo cp ../etc/usbshare.service /etc/systemd/system

echo "### Installation of service for log files management"
sudo cp log_manager.py /usr/local/share
sudo cp ../etc/logmanager.service /etc/systemd/system

echo "### Enabling of installed services"
cd /usr/local/share/
sudo chmod +x usb_share.py
sudo chmod +x log_manager.py

cd /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable usbshare.service
sudo systemctl start usbshare.service
sudo systemctl enable logmanager.service
sudo systemctl start logmanager.service

echo "### Installing dependencies for SAMBA"
sudo apt-get install samba samba-common-bin
sudo chmod -R 777 /etc/samba/smb.conf

echo "### Configuring SAMBA"
echo "[share]" >> /etc/samba/smb.conf
echo "Comment = Shared Folder" >> /etc/samba/smb.conf
echo "Path = /mnt/usb_share" >> /etc/samba/smb.conf
echo "Browseable = yes" >> /etc/samba/smb.conf
echo "Writeable = Yes" >> /etc/samba/smb.conf
echo "only guest = no" >> /etc/samba/smb.conf
echo "create mask = 0777" >> /etc/samba/smb.conf
echo "directory mask = 0777" >> /etc/samba/smb.conf
echo "Public = yes" >> /etc/samba/smb.conf
echo "Guest ok = yes" >> /etc/samba/smb.conf

echo "### Restarting SAMBA"
sudo /etc/init.d/samba restart

echo "### Installation completed, rebooting in 3 seconds"
sleep 3

#sudo reboot
