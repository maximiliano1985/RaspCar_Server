CHIP Auto-Shutdown
============================

This script will monitor battery voltage and when it drops below a specified threshold it will shutdown CHIP.
It can be installed as a service so frequent battery polling is possible.
Charging state changes are logged to syslog.

# Installation
Install the script:
  ```
  cd chip_autoshutdown
  sudo cp ./chip_autoshutdown.sh /usr/bin/
  ```
Install systemd service (so it runs at boot):
  ```
  sudo cp ./chip_autoshutdown.service /lib/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable chip_autoshutdown.service
  ```
Start it:
  ```
  sudo systemctl start chip_autoshutdown.service
  ```
  
