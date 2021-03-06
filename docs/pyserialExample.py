import serial
import time

def read_serial(ser):
    gps_word = ''
    ch = ''
    while ch != '\r':
        ch = ser.read()
        gps_word += ser.read()
        print(gps_word)
    return gps_word

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 19200)#,
    #parity=serial.PARITY_NONE,
    #stopbits=serial.STOPBITS_ONE,
    #bytesize=serial.EIGHTBITS,
    #timeout=1)

START_TIME_S = time.time()
t = 0
while t < 3:        
    line = ser.readline()
    t = time.time()-START_TIME_S
    print(round(t, 3), line)


