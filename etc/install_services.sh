echo "### INSTALLING SERVICES ###"

echo "### Installation of service for automatic USB management"
sudo cp usb_share.py /usr/local/share
sudo cp ../etc/usbshare.service /etc/systemd/system

echo "### Installation of service for automatic OBD management"
sudo cp obd_logger.py /usr/local/share
sudo cp obd_connect.py /usr/local/share
sudo cp ../etc/obdlogger.service /etc/systemd/system
sudo cp ../etc/obdconnect.service /etc/systemd/system

echo "### Installation of service for log files management"
#sudo cp log_manager.py /usr/local/share
#sudo cp ../etc/logmanager.service /etc/systemd/system

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

#sudo systemctl enable usbshare.service
#sudo systemctl start usbshare.service

sudo systemctl enable obdlogger.service
sudo systemctl start obdlogger.service

sudo systemctl enable logmanager.service
sudo systemctl start logmanager.service
