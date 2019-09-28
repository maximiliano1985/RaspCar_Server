echo "### INSTALLING SERVICES ###"

echo "### Installation of service for automatic USB management"
sudo cp ../lib/smartMassUSB.py      /usr/local/share
sudo cp ../etc/smartmassusb.service /etc/systemd/system

echo "### Installation of service for battery management"
sudo cp ../lib/powerManagement.py /usr/local/share
sudo cp ../etc/powermanagement.service /etc/systemd/system

echo "### Installation of service for automatic data recording"
sudo cp ../lib/dataRecorder.py 	  /usr/local/share
sudo cp ../etc/datarecorder.service /etc/systemd/system

echo "### Installation of service for automatic obd connecting"
sudo cp ../lib/obd_connect.py     /usr/local/share
sudo cp ../etc/obdconnect.service /etc/systemd/system

echo "### Installation of service for log file monitoring"
sudo cp logManager.py      		  /usr/local/share
sudo cp ../etc/logmanager.service /etc/systemd/system

echo "### Installation of libraries"
sudo cp ../lib/fileLogger.py 	  /usr/local/share
sudo cp ../lib/obdRecorder.py     /usr/local/share
sudo cp ../lib/gpsRecorder.py     /usr/local/share

echo "### Enabling installed services"
cd /usr/local/share/
sudo chmod +x smartMassUSB.py
sudo chmod +x powerManagement.py
sudo chmod +x dataRecorder.py
sudo chmod +x obd_connect.py
sudo chmod +x logManager.py

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
#sudo rm -rf /usr/local/share/smartMassUSB.py
#sudo rm -rf /usr/local/share/powerManagement.py
#sudo rm -rf /usr/local/share/dataRecorder.py
#sudo rm -rf /usr/local/share/logManager.py
#
#sudo systemctl stop dataRecorder
#sudo systemctl disable dataRecorder
#sudo rm /etc/systemd/system/dataRecorder.service
#
#sudo systemctl stop powerManagement
#sudo systemctl disable powerManagement
#sudo rm /etc/systemd/system/powerManagement.service
#
#sudo systemctl stop smartMassUSB
#sudo systemctl disable smartMassUSB
#sudo rm /etc/systemd/system/smartMassUSB.service
#
#sudo systemctl stop logManager
#sudo systemctl disable logManager
#sudo rm /etc/systemd/system/logManager
#
#sudo systemctl daemon-reload
#sudo systemctl reset-failed



