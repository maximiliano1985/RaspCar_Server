#!/usr/bin/python3
import time
import signal
import serial


def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

class gpsRecorder(object):
    
    def __init__(self, port='/dev/ttyS0', baudrate = 19200, debug = False):
       self.debug = debug
       
       #self.header = "time_gps;status_gps;latitude_gps;NS_indic_gps;longitude_gps;EW_indic_gps;speed_gps;course_gps;utc_gps;mode_gps;"
       
       self.serialConnection = serial.Serial(
           port=port,
           baudrate = baudrate)#,
           #parity=serial.PARITY_NONE,
           #stopbits=serial.STOPBITS_ONE,
           #bytesize=serial.EIGHTBITS,
           #timeout=1)
    
    def read_once(self):
        line = self.serialConnection.readline()
        # $GPRMC,hhmmss.sss,A,dddmm.mmmm,a,dddmm.mmmm,a,x.x,x.x,ddmmyy,,,a*hh<CR><LF>
        #   time: in hhmmss.sss
        #   status: V = Navigation receiver warning, A = Data Valid
        #   latitude: dddmm.mmmm 
        #   NS_indic: N north, S south
        #   longitude: dddmm.mmmm 
        #   EW_indic: E east, W west
        #   speed: Speed over ground in knots
        #   course: Course over ground in degrees
        #   utc: UTC date of position fix, ddmmyy format
        #   mode: Mode indicator N = Data not valid,
        #                        A = Autonomous mode,
        #                        D = Differential mode,
        #                        E = Estimated (dead reckoning) mode,
        #                        M = Manual input mode,
        #                        S = Simulator mode
        if self.debug:
            print(line)
        return [time, status, latitude, NS_indic, longitude, EW_indic, speed, course, utc, mode]
            
    def read(self):
        while True:        
            self.read_once()

if __name__ == '__main__':
    
    rec = gpsRecorder(port='/dev/ttyS0', baudrate = 19200, debug = True)
    rec.read_once()