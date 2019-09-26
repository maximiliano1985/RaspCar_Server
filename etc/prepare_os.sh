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
sudo pip3 instecho
#sudo pip3 install git+git://github.com/chrisb2/pi_ina219.git
#sudo pip3 install adafruit-blinka
sudo pip3 install pi-ina219

sudo pip3 install circuitpython-build-tools

echo "### Creating folder for logs (available only for pi user)"
sudo mkdir /home/pi/Documents
sudo mkdir /home/pi/Documents/logs
sudo mkdir /home/pi/Documents/logs/usb_share
sudo mkdir /home/pi/Documents/logs/recorder_logs
sudo mkdir /home/pi/Documents/logs/recorderdata_logs
sudo mkdir /home/pi/Documents/logs/powmngm_logs

sudo chmod -R 777 /home/pi/Documents
