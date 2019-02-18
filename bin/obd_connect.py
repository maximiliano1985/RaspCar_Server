import subprocess
import time

# ELM327 v1.5
while True:
    subprocess.call("sudo rfcomm connect 0 00:0D:18:3A:67:89 1", shell=True)
    time.sleep(15)