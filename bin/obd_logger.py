#!/usr/bin/python3
import obd
import time
import getpass
import subprocess
import datetime

# ELM327 v1.5
#subprocess.Popen("sudo rfcomm connect 0 00:0D:18:3A:67:89 1", shell=True)


## Logger management
HOME_FOLDER     = '/home/'+getpass.getuser()
LOG_FOLDER      = HOME_FOLDER+"/Documents/logs/obd_logs/"
LOGDATA_FOLDER  = HOME_FOLDER+"/Documents/logs/obddata_logs/"
LOG_FILENAME    = "_obd.log"
LOGDATA_FILENAME= "_obdData.log"
LOG_TOKEN       = "[O]"#"[USB_SHARE]"
LOG_SEP         = ";"

RECONNECTION_DELAY_SEC  = 20
RECONNECTION_MAX_TRIALS = 20

LOGDATA_FILE    = None
LOG_FILE        = None

VEROBSE = False

def write_to_log(msg, printTime = True):
    global LOG_FILENAME
    now = datetime.datetime.now()
    hms = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
    log_file = open(LOG_FOLDER+LOG_FILENAME, 'a')
    log_file.write(hms + " " + LOG_TOKEN + " " + msg + '\n')
    log_file.close() 

def write_to_logData(msg, printTime = True):
    global LOGDATA_FILE
    now = datetime.datetime.now()
    hms = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
    LOGDATA_FILE.write(hms + msg + '\n')
   
def init_LOG_FILEs(header):
    global LOG_FILENAME
    global LOGDATA_FILE
    now = datetime.datetime.now()
    timenow = str(now)
    timenow = timenow.replace(' ', 'h')
    timenow = timenow.replace(':', '_')
    #print(timenow)
    LOGDATA_FILE = open(LOGDATA_FOLDER+timenow+LOGDATA_FILENAME, 'a')
    LOG_FILENAME = timenow+LOG_FILENAME
    
    write_to_logData(header, False)
    
    
    
port = '/dev/rfcomm0'
OBDconnection = obd.OBD(port) 

cmds = [
    obd.commands.THROTTLE_POS,#
    obd.commands.RELATIVE_THROTTLE_POS,#
    obd.commands.SPEED, #
    obd.commands.RPM, #
    obd.commands.ENGINE_LOAD,# %
    obd.commands.FUEL_LEVEL,#
    obd.commands.COOLANT_TEMP,#
    #obd.commands.FUEL_PRESSURE,
    #obd.commands.TIMING_ADVANCE,
    obd.commands.AMBIANT_AIR_TEMP,
    obd.commands.INTAKE_PRESSURE,
    obd.commands.INTAKE_TEMP,
    obd.commands.MAF,# gps
    #obd.commands.FUEL_RAIL_PRESSURE_VAC,
    obd.commands.FUEL_RAIL_PRESSURE_DIRECT,
    #obd.commands.COMMANDED_EGR,
    obd.commands.BAROMETRIC_PRESSURE,
    obd.commands.CONTROL_MODULE_VOLTAGE,
    #obd.commands.ABSOLUTE_LOAD,
    #obd.commands.COMMANDED_EQUIV_RATIO,
    #obd.commands.THROTTLE_POS_B,
    #obd.commands.THROTTLE_POS_C,
    obd.commands.ACCELERATOR_POS_D,# % throttle
    obd.commands.ACCELERATOR_POS_E,# % throttle
    #obd.commands.ACCELERATOR_POS_F,
    obd.commands.THROTTLE_ACTUATOR, # %
    obd.commands.OIL_TEMP
    #obd.commands.FUEL_RATE
]


#response = OBDconnection.query(obd.commands.ELM_VERSION); print(response)


header = "Time"
for cmd in cmds:
    header += LOG_SEP + cmd.name

init_LOG_FILEs(header)

nDatalines = 0



n_reconnection_trials = 0
while not OBDconnection.is_connected():
    write_to_log("Not connected, reconnecting in "+str(RECONNECTION_DELAY_SEC)+" seconds")
    time.sleep(RECONNECTION_DELAY_SEC)
    
    OBDconnection = obd.OBD(port) 
    
    n_reconnection_trials += 1
    if n_reconnection_trials > RECONNECTION_MAX_TRIALS:
        write_to_log("Impossible to connect, quit application")
        quit()
    

if OBDconnection.is_connected():
    while True:
        write_to_log("Connected to "+port)
        logged_values = ""
        for cmd in cmds:
            response = OBDconnection.query(cmd)
            logged_values += LOG_SEP + str(response.value.magnitude)
            
        if VEROBSE:
            print(logged_values)    
    
        write_to_logData(logged_values)
        
        nDatalines += 1
        if (nDatalines % 1000) == 0:
            write_to_log("Logged "+str(nDatalines)+" lines")
    
    OBDconnection.close()
   
    LOGDATA_FILE.close()    
