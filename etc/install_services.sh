echo "### INSTALLING SERVICES ###"

echo "### Installation of service for automatic USB management"
sudo cp ../lib/smartMassUSB.py      /usr/local/share
sudo cp ../etc/smartMassUSB.service /etc/systemd/system

echo "### Installation of service for automatic OBD management"
sudo cp ../lib/dataRecorder.py 	  /usr/local/share
sudo cp ../etc/dataRecorder.service /etc/systemd/system

sudo cp ../lib/obdRecorder.py     /usr/local/share
sudo cp ../lib/gpsRecorder.py     /usr/local/share

sudo cp ../lib/obd_connect.py     /usr/local/share
sudo cp ../etc/obdconnect.service /etc/systemd/system

echo "### Installation of service for log files management"
sudo cp ../lib/logManager.py      /usr/local/share
sudo cp ../etc/logManager.service /etc/systemd/system

echo "### Installation of service for battery management"
sudo cp ../lib/powerManagement.py /usr/local/share
sudo cp ../etc/powerManagement.service /etc/systemd/system

echo "### Installation of libraries"
sudo cp ../lib/fileLogger.py /usr/local/share

echo "### Enabling installed services"
cd /usr/local/share/
sudo chmod +x smartMassUSB.py
sudo chmod +x logManager.py
sudo chmod +x obd_connect.py
sudo chmod +x dataRecorder.py
sudo chmod +x powerManagement.py

cd /etc/systemd/system
sudo systemctl daemon-reload

sudo systemctl enable smartMassUSB.service
sudo systemctl start  smartMassUSB.service

sudo systemctl enable dataRecorder.service
sudo systemctl start  dataRecorder.service

sudo systemctl enable logManager.service
sudo systemctl start  logManager.service

sudo systemctl enable powerManagement.service
sudo systemctl start  powerManagement.service

#######
#sudo rm -rf /usr/local/share/usb_share.py
#sudo rm -rf /usr/local/share/battery_manager.py
#sudo rm -rf /usr/local/share/obd_logger.py
#sudo rm -rf /usr/local/share/log_manager.py
#
#sudo systemctl stop obdlogger
#sudo systemctl disable obdlogger
#sudo rm /etc/systemd/system/obdlogger.service
#
#sudo systemctl stop batterymanager
#sudo systemctl disable batterymanager
#sudo rm /etc/systemd/system/batterymanager.service
#
#sudo systemctl stop usbshare
#sudo systemctl disable usbshare
#sudo rm /etc/systemd/system/usbshare.service
#
#sudo systemctl stop log_manager
#sudo systemctl disable log_manager
#sudo rm /etc/systemd/system/log_manager
#
#sudo systemctl daemon-reload
#sudo systemctl reset-failed
#


