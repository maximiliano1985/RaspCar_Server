echo "### INSTALLING MEMORY ###"

SIZE_VIRTUAL_MEMORY=20000 # Mbyte

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
