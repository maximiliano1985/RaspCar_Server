#!/usr/bin/python3
import time
import os
import getpass
from watchdog.observers import Observer
from watchdog.events import *

import sys
sys.path.insert(0, '../lib')
from fileLogger import fileLogger

CMD_MOUNT = "modprobe g_mass_storage file=/piusb.bin stall=0 ro=1 removable=1"
CMD_UNMOUNT = "modprobe -r g_mass_storage"
CMD_SYNC = "sync"

WATCH_PATH = "/mnt/usb_share"
ACT_EVENTS = [DirDeletedEvent, DirMovedEvent, FileDeletedEvent, FileModifiedEvent, FileMovedEvent]
ACT_TIME_OUT = 30 # s

############################################
class DirtyHandler(FileSystemEventHandler):
    def __init__(self):
        self.reset()

    def on_any_event(self, event):
        if type(event) in ACT_EVENTS:
            #write_msg_to_log("Accessed to files in mass storage: " + str(type(event)))
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
############################################

### RUN ###
flog = fileLogger(
    log_folder      = "/home/pi/Documents/logs/usb_share/",
    log_filetoken   = "_usb_share.log",
    log_sep         = " ",
    log_token       = "[U]")

os.system(CMD_MOUNT)
flog.write_msg_to_log("Initial mounting of mass storage")

evh = DirtyHandler()
observer = Observer()
observer.schedule(evh, path=WATCH_PATH, recursive=True)
observer.start()
flog.write_msg_to_log("Started mass storage manager")

try:
    while True:
        while evh.dirty:
            time_out = time.time() - evh.dirty_time

            if time_out >= ACT_TIME_OUT:
                flog.write_msg_to_log("No uploads detected in mass storage")
                
                os.system(CMD_UNMOUNT)
                flog.write_msg_to_log("Disconnected mass storage")
                time.sleep(1)
                
                os.system(CMD_SYNC)
                flog.write_msg_to_log("Syncronized files in mass storage")
                time.sleep(1)
                
                os.system(CMD_MOUNT)
                flog.write_msg_to_log("Mounted mass storage")
                evh.reset()

            time.sleep(1)

        time.sleep(1)
        
except KeyboardInterrupt:
    observer.stop()
    flog.write_msg_to_log("KeyboardInterrupt on mass storage manager")
    observer.join()
