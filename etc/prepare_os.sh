echo "### PREPARING OS ###"

echo "### Cleaning the OS installation"
sudo apt-get clean
sudo apt-get autoremove -y

echo "### Installing dependencies for automatic USB management"
sudo apt-get install python3-pip -y
sudo pip3 install --upgrade setuptools
sudo pip3 install watchdog
sudo pip3 install datetime
sudo pip3 install obd

echo "### Creating folder for logs (available only for pi user)"
sudo mkdir /home/pi/Documents
sudo mkdir /home/pi/Documents/logs
sudo mkdir /home/pi/Documents/logs/usb_share
sudo mkdir /home/pi/Documents/logs/obd_logs
sudo mkdir /home/pi/Documents/logs/obddata_logs
sudo chmod -R 777 /var/www/owncloud
