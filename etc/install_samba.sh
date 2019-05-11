echo "### INSTALLING SAMBA ###"

echo "### Installing dependencies for SAMBA"
sudo apt-get install samba samba-common-bin
sudo chmod -R 777 /etc/samba/smb.conf

echo "### Configuring SAMBA"
echo "[music]" >> /etc/samba/smb.conf
echo "  Comment = Music Folder" >> /etc/samba/smb.conf
echo "  Path = /mnt/usb_share" >> /etc/samba/smb.conf
echo "  Browseable = yes" >> /etc/samba/smb.conf
echo "  Writeable = Yes" >> /etc/samba/smb.conf
echo "  only guest = no" >> /etc/samba/smb.conf
echo "  create mask = 0777" >> /etc/samba/smb.conf
echo "  directory mask = 0777" >> /etc/samba/smb.conf
echo "  Public = yes" >> /etc/samba/smb.conf
echo "  Guest ok = yes" >> /etc/samba/smb.conf
echo "" >> /etc/samba/smb.conf
echo "[logs]" >> /etc/samba/smb.conf
echo "  Comment = Logs Folder" >> /etc/samba/smb.conf
echo "  Path = /var/www/owncloud/data/owncloud/files/logs/" >> /etc/samba/smb.conf
echo "  Browseable = yes" >> /etc/samba/smb.conf
echo "  Writeable = Yes" >> /etc/samba/smb.conf
echo "  only guest = no" >> /etc/samba/smb.conf
echo "  create mask = 0777" >> /etc/samba/smb.conf
echo "  directory mask = 0777" >> /etc/samba/smb.conf
echo "  Public = yes" >> /etc/samba/smb.conf
echo "  Guest ok = yes" >> /etc/samba/smb.conf

echo "### Restarting SAMBA"
sudo /etc/init.d/samba restart
