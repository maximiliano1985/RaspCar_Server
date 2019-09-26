#!/usr/bin/python3
import time
import datetime
import os
import getpass
from watchdog.observers import Observer
from watchdog.events import *

from fileLogger import fileLogger

class smartMassUSB(Object):
    def __init__(self, watch_path = "/mnt/usb_share", file_logger = fileLogger(), verbose = False):
        self.file_logger    = file_logger
        self.file_logger.write_msg_to_log("Initializing")
        
        self.CMD_MOUNT      = "modprobe g_mass_storage file=/piusb.bin stall=0 ro=1 removable=1"
        self.CMD_UNMOUNT    = "modprobe -r g_mass_storage"
        self.CMD_SYNC       = "sync"
        self.verbose        = verbose
        
        self.WATCH_PATH     = watch_path
        self.ACT_EVENTS     = [DirDeletedEvent, DirMovedEvent, FileDeletedEvent,
                                FileModifiedEvent, FileMovedEvent]
        self.ACT_TIME_OUT   = 30 # s
        
        self.file_logger.write_msg_to_log("Usb mounted")
        if self.verbose:
            print("Initial mounting of usb mass storage")
        os.system(self.CMD_MOUNT)
        
        self.observer = Observer(verbose)
        
    def close():
        self.file_logger.close()
        
    def run(self):
        self.file_logger.write_msg_to_log("Started usb mass storage manager")
        if self.verbose:
            print("Started usb mass storage manager")
        
        
        evh = DirtyHandler()
        self.observer.schedule(evh, path=self.WATCH_PATH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
                
                while evh.dirty:
                    time.sleep(1)
                    time_out = time.time() - evh.dirty_time
                    
                    if time_out >= self.ACT_TIME_OUT:
                        self.file_logger.write_msg_to_log("No uploads detected")
                        if self.verbose:
                            print("No uploads detected in mass storage")
                        
                        os.system(self.CMD_UNMOUNT)
                        self.file_logger.write_msg_to_log("Disconnected usb mass storage")
                        if self.verbose:
                            print("Disconnected mass storage")
                        time.sleep(1)
                            
                        os.system(self.CMD_SYNC)
                        self.file_logger.write_msg_to_log("Syncronized files in mass storage")
                        if self.verbose:
                            print("Syncronized files in usb mass storage")
                        time.sleep(1)
                        
                        os.system(self.CMD_MOUNT)
                        self.file_logger.write_msg_to_log("Usb mounted")
                        if self.verbose:
                            print("Mounted usb mass storage")
                            
                        evh.reset()
                            
       except KeyboardInterrupt:
           self.file_logger.write_msg_to_log("User interrupt of usb mass manager")
           if self.verbose:
               print("KeyboardInterrupt on usb mass storage manager")
           self.observer.stop()
           self.observer.join()        

class DirtyHandler(FileSystemEventHandler):
    def __init__(self, verbose = False):
        self.reset()
        self.verbose = verbose

    def on_any_event(self, event):
        if type(event) in self.ACT_EVENTS:
            if self.verbose:
                print("Accessed to files in mass storage: " + str(type(event)))
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


if __name__ == '__main__':
    flog = fileLogger(
        log_folder      = "/home/pi/Documents/logs/usb_share/",
        log_filetoken   = "_usb_share.log",
        log_sep         = " ",
        log_token       = "[U]")
        
    usb = smartMassUSB( file_logger = flog, verbose = True )
    usb.run
    