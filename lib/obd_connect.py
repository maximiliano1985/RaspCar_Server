#!/usr/bin/python3
import subprocess
import time
import sys

# ELM327 v1.5
#subprocess.call("Pair 00:0D:18:3A:67:89 1", shell=True)

while True:
    try:
        subprocess.call("sudo rfcomm connect 0 00:0D:18:3A:67:89 1", shell=True)
        #sudo rfcomm connect hci0 00:0D:18:3A:67:89
        time.sleep(60)
    except:
        print("OBD connect unexpected error: "+str(sys.exc_info()[0]))
    time.sleep(60)