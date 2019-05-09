#!/usr/bin/python3
import time
import datetime
import os
import getpass
from watchdog.observers import Observer
from watchdog.events import *

CMD_MOUNT = "modprobe g_mass_storage file=/piusb.bin stall=0 ro=1 removable=1"
CMD_UNMOUNT = "modprobe -r g_mass_storage"
CMD_SYNC = "sync"

WATCH_PATH = "/mnt/usb_share"
ACT_EVENTS = [DirDeletedEvent, DirMovedEvent, FileDeletedEvent, FileModifiedEvent, FileMovedEvent]
ACT_TIME_OUT = 30 # s

## Logger management
HOME_FOLDER     = '/home/chip'#+getpass.getuser()
LOG_FOLDER      = HOME_FOLDER+"/Documents/logs/usb_share/"
LOG_TOKEN       = "[U]"#"[USB_SHARE]"
LOG_SEP         = " "
LOG_FILENAME    = None

def init_log_file():
    global LOG_FILENAME
    now = datetime.datetime.now()
    timenow = str(now)
    timenow = timenow.replace(' ', 'h')
    timenow = timenow.replace(':', '_')
    #print(timenow)
    LOG_FILENAME = timenow+"_usb_share.log"
    
def write_to_log(msg):
    now = datetime.datetime.now()
    hms = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
    log_file = open(LOG_FOLDER+LOG_FILENAME, 'a')
    log_file.write(hms + LOG_SEP + LOG_TOKEN + LOG_SEP + msg + '\n')
    log_file.close()
    
##

class DirtyHandler(FileSystemEventHandler):
    def __init__(self):
        self.reset()

    def on_any_event(self, event):
        if type(event) in ACT_EVENTS:
            write_to_log("Accessed to files in mass storage: " + str(type(event)))
            self._dirty = True
            self._dirty_time = time.time()

    @property
    def dirty(self):
        return self._dirty

    @property
    def dirty_time(self):
        return self._dirty_time

    def reset(self):
        self._dirty = False
        self._dirty_time = 0
        self._path = None


### RUN ###

init_log_file()

os.system(CMD_MOUNT)
write_to_log("Initial mounting of mass storage")

evh = DirtyHandler()
observer = Observer()
observer.schedule(evh, path=WATCH_PATH, recursive=True)
observer.start()
write_to_log("Started mass storage manager")

try:
    while True:
        while evh.dirty:
            time_out = time.time() - evh.dirty_time

            if time_out >= ACT_TIME_OUT:
                write_to_log("No uploads detected in mass storage")
                os.system(CMD_UNMOUNT)
                write_to_log("Disconnected mass storage")
                time.sleep(1)
                os.system(CMD_SYNC)
                write_to_log("Syncronized files in mass storage")
                time.sleep(1)
                os.system(CMD_MOUNT)
                write_to_log("Mounted mass storage")
                evh.reset()

            time.sleep(1)

        time.sleep(1)
        
except KeyboardInterrupt:
    observer.stop()
    write_to_log("KeyboardInterrupt on mass storage manager")
    

observer.join()
