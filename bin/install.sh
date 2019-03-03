case $1 in

	"-a")
		sudo sh ../etc/prepare_os.sh
		sudo sh ../etc/install_memory.sh
		sudo sh ../etc/install_services.sh
		sudo sh ../etc/install_samba.sh
		
		echo "### Installation completed, rebooting in 3 seconds"
		sleep 3
		break
		;;
		
	"-p")
		sudo sh ../etc/prepare_os.sh
		break
		;;
			
	"-m")
		sudo sh ../etc/install_memory.sh
		break
		;;
		
	"-s")
		sudo sh ../etc/install_services.sh
		break
		;;
	
	"-c")
		sudo sh ../etc/install_samba.sh
		break
		;;
	
	*) #### HELP ####
	echo "### HELP ###\n"
	echo "   -a : install all automatically"
	echo "   -p : prepare the system"
	echo "   -m : prepare shared memory blocks"
	echo "   -s : install services"
	echo "   -c : install samba cloud server"
	echo "\nNote: for manual installation follow order -p, -m, -s, -c"
esac


#sudo reboot
