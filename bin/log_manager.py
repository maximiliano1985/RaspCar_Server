#!/usr/bin/python3
# This scripts appends to a unique log file the log files generated by the following scripts (services):
# - usb_share.py
# - obd_log.py (TBD)



import glob
import time
import datetime
import os
import subprocess
import select
import getpass

## Logger management
HOME_FOLDER     = '/home/pi'#+getpass.getuser()
LOG_FOLDER      = HOME_FOLDER+"/Documents/logs/"
LOG_TOKEN       = "[L]"
LOG_SEP         = " "
LOG_FILENAME    = None

LOG_FOLDER_USBSHARE = LOG_FOLDER+"usb_share/"
LOG_FOLDER_OBDLOG   = LOG_FOLDER+"obd_logs/"

SEM_RED   = False
SEM_GREEN = True
SEMAPHORE = SEM_GREEN

def init_log_file():
    global LOG_NLINES
    global LOG_FILENAME
    
    now = datetime.datetime.now()
    timenow = str(now)
    timenow = timenow.replace(' ', 'h')
    timenow = timenow.replace(':', '_')
    #print(timenow)
    LOG_FILENAME = timenow+".log"

    
def write_to_log(msg):    
    log_file = open(LOG_FOLDER+LOG_FILENAME, 'a')
    outstr = LOG_SEP + str(msg) + '\n'
    print(outstr, end="")
    log_file.write(outstr)
    log_file.close()
    
##

def process_log_file(f_log):
    global SEMAPHORE
    # if someone else is writing in the main log file, wait until the semaphore is released
    while SEMAPHORE == SEM_RED:
        sleep(0.0001)
    if SEMAPHORE == SEM_GREEN:
        SEMAPHORE = SEM_RED
        log_line = f_log.stdout.readline()
        write_to_log(log_line)
        SEMAPHORE = SEM_GREEN


### RUN ###

init_log_file()


try:
    
    time.sleep(10)
    
    # get the newest file
    print(LOG_FOLDER_USBSHARE+'.2*.log')
    newestfile_usb = max(glob.iglob(LOG_FOLDER_USBSHARE+'.2*.log'), key=os.path.getctime)
    newestfile_obd = max(glob.iglob(LOG_FOLDER_OBDLOG+'2*.log'), key=os.path.getctime)
    
    write_to_log(LOG_TOKEN+" Logs manager monitoring file "+newestfile_usb)
    write_to_log(LOG_TOKEN+" Logs manager monitoring file "+newestfile_obd)
    
    f_usb = subprocess.Popen(['tail','-F',newestfile_usb],\
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p_usb = select.poll()
    p_usb.register(f_usb.stdout)
    
    f_obd = subprocess.Popen(['tail','-F',newestfile_obd],\
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p_obd = select.poll()
    p_obd.register(f_obd.stdout)
    
    while True:
        if p_usb.poll(1):
            process_log_file(f_usb)
            process_log_file(f_obd) 
             
        #time.sleep(1)
except KeyboardInterrupt:
    write_to_log(LOG_TOKEN+" KeyboardInterrupt logs manager")
