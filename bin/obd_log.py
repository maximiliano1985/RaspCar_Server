#!/usr/bin/python3
# TOBEDONE



import time
import datetime
import os



## Logger management
HOME_FOLDER     = "/home/pi/"
LOG_FOLDER      = HOME_FOLDER+"Documents/logs/"
LOG_TOKEN       = "[LOGGER]"
LOG_SEP         = " "
LOG_FILENAME    = None
LOG_MAXNLINES   = 10000
LOG_NLINES      = 0

def init_log_file():
    global LOG_NLINES
    global LOG_FILENAME
    
    now = datetime.datetime.now()
    timenow = str(now)
    timenow = timenow.replace(' ', 'h')
    timenow = timenow.replace(':', '_')
    #print(timenow)
    LOG_FILENAME = "."+timenow+".log"
    LOG_NLINES   = 0
    
def write_to_log(msg):
    global LOG_NLINES
    global LOG_FILENAME
    if LOG_NLINES == LOG_MAXNLINES:
        init_log_file()
    
    now = datetime.datetime.now()
    log_file = open(LOG_FOLDER+LOG_FILENAME, 'a')
    log_file.write(str(now) + LOG_SEP + LOG_TOKEN + LOG_SEP + msg + '\n')
    log_file.close()
    LOG_NLINES += 1
    
##


### RUN ###

init_log_file()


try:
    while True:
        
except KeyboardInterrupt:
    observer.stop()
    write_to_log("KeyboardInterrupt on mass storage manager")
