#!/usr/bin/python3
import subprocess
import time
import sys

# ELM327 v1.5
while True:
    try:
        subprocess.call("sudo rfcomm connect 0 00:0D:18:3A:67:89 1", shell=True)
    except:
        print("OBD connect unexpected error: "+str(sys.exc_info()[0]))
    time.sleep(15)