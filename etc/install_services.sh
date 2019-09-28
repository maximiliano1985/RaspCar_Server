echo "### INSTALLING SERVICES ###"

echo "### Installation of service for automatic USB management"
sudo cp ../lib/smartmassusb.py      /usr/local/share
sudo cp ../etc/smartmassusb.service /etc/systemd/system

echo "### Installation of service for battery management"
sudo cp ../lib/powermanagement.py /usr/local/share
sudo cp ../etc/powermanagement.service /etc/systemd/system

echo "### Installation of service for automatic data recording"
sudo cp ../lib/datarecorder.py 	  /usr/local/share
sudo cp ../etc/datarecorder.service /etc/systemd/system

echo "### Installation of service for automatic obd connecting"
sudo cp ../lib/obd_connect.py     /usr/local/share
sudo cp ../etc/obdconnect.service /etc/systemd/system

echo "### Installation of service for log file monitoring"
sudo cp logmanager.py      		  /usr/local/share
sudo cp ../etc/logmanager.service /etc/systemd/system

echo "### Installation of libraries"
sudo cp ../lib/fileLogger.py 	  /usr/local/share
sudo cp ../lib/obdRecorder.py     /usr/local/share
sudo cp ../lib/gpsRecorder.py     /usr/local/share

echo "### Enabling installed services"
cd /usr/local/share/
sudo chmod +x smartmassusb.py
sudo chmod +x powermanagement.py
sudo chmod +x datarecorder.py
sudo chmod +x obd_connect.py
sudo chmod +x logmanager.py

cd /etc/systemd/system
sudo systemctl daemon-reload

sudo systemctl enable smartmassusb.service
sudo systemctl start  smartmassusb.service

sudo systemctl enable powermanagement.service
sudo systemctl start  powermanagement.service

sudo systemctl enable datarecorder.service
sudo systemctl start  datarecorder.service

sudo systemctl enable obdconnect.service
sudo systemctl start  obdconnect.service

sudo systemctl enable logmanager.service
sudo systemctl start  logmanager.service


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


