echo "### PREPARING OS ###"
sudo apt-get update

echo "### Cleaning the OS installation"
sudo apt-get clean
sudo apt-get autoremove -y

#sudo apt-get install python3-gpiozero
sudo apt-get install python3-smbus
sudo apt-get install i2c-tools

echo "### Installing dependencies for automatic USB management"
sudo apt-get install python3-pip -y
sudo pip3 install --upgrade setuptools
sudo pip3 install watchdog
sudo pip3 install datetime
sudo pip3 install obd
#sudo pip3 install gpiozero
sudo pip3 instecho "### INSTALLING SERVICES ###"

echo "### Installation of service for automatic USB management"
sudo cp usb_share.py /usr/local/share
sudo cp ../etc/usbshare.service /etc/systemd/system

echo "### Installation of service for automatic OBD management"
sudo cp obd_logger.py /usr/local/share
sudo cp obd_connect.py /usr/local/share
sudo cp ../etc/obdlogger.service /etc/systemd/system
sudo cp ../etc/obdconnect.service /etc/systemd/system

echo "### Installation of service for log files management"
sudo cp log_manager.py /usr/local/share
sudo cp ../etc/logmanager.service /etc/systemd/system

echo "### Installation of service for battery management"
sudo cp battery_status_i2c.py /usr/local/share
sudo cp ../etc/batterymanager.service /etc/systemd/system


echo "### Enabling installed services"
cd /usr/local/share/
sudo chmod +x usb_share.py
sudo chmod +x log_manager.py
sudo chmod +x obd_connect.py
sudo chmod +x obd_logger.py

cd /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable obdconnect.service
sudo systemctl start obdconnect.service

sudo systemctl enable usbshare.service
sudo systemctl start usbshare.service

sudo systemctl enable obdlogger.service
sudo systemctl start obdlogger.service

sudo systemctl enable logmanager.service
sudo systemctl start logmanager.service
all smbus

echo "### Creating folder for logs (available only for pi user)"
sudo mkdir /home/pi/Documents
sudo mkdir /home/pi/Documents/logs
sudo mkdir /home/pi/Documents/logs/usb_share
sudo mkdir /home/pi/Documents/logs/obd_logs
sudo mkdir /home/pi/Documents/logs/obddata_logs
sudo chmod -R 777 /home/pi/Documents
