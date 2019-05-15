#!/usr/bin/python3
import obd
import time
import getpass
#import subprocess
import datetime
import sys

# ELM327 v1.5
#subprocess.Popen("sudo rfcomm connect 0 00:0D:18:3A:67:89 1", shell=True)


## Logger management
LOG_FOLDER      = "/var/www/owncloud/data/raspi/files/logs/obd_logs/"
                    # HOME_FOLDER+"/Documents/logs/obd_logs/"
LOGDATA_FOLDER  = "/var/www/owncloud/data/raspi/files/logs/obddata_logs/"
                    # HOME_FOLDER+"/Documents/logs/obddata_logs/"
LOG_FILENAME    = "_obd.log"
LOGDATA_FILENAME= "_obdData.log"
LOG_TOKEN       = "[O]"#"[USB_SHARE]"
LOG_SEP         = ";"

RECONNECTION_DELAY_SEC  = 10
RECONNECTION_MAX_TRIALS = 20

LOGDATA_FILE    = None
LOG_FILE        = None

VERBOSE = True

def write_to_log(msg, printTime = True):
    global LOG_FILENAME
    now = datetime.datetime.now()
    hms = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
    log_file = open(LOG_FOLDER+LOG_FILENAME, 'a')
    log_file.write(hms + " " + LOG_TOKEN + " " + msg + '\n')
    log_file.close() 

def write_to_logData(msg, logdata_file, printTime = True):
    now = datetime.datetime.now()
    hms = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
    if printTime:
        logdata_file.write(hms + msg + '\n')
    else:
        logdata_file.write(msg + '\n')
   
def init_LOG_FILEs():
    global LOG_FILENAME
    global LOGDATA_FILE
    now = datetime.datetime.now()
    timenow = str(now)
    timenow = timenow.replace(' ', 'h')
    timenow = timenow.replace(':', '_')
    #print(timenow)
    LOGDATA_FILE = open(LOGDATA_FOLDER+timenow+LOGDATA_FILENAME, 'a')
    LOG_FILENAME = timenow+LOG_FILENAME
    

def reconnect():
    OBDconnection = obd.OBD(port) 
    
    n_reconnection_trials = 0

    
    while not OBDconnection.is_connected():
        n_reconnection_trials += 1
        write_to_log(str(n_reconnection_trials)+" Not connected, reconnecting in "+str(RECONNECTION_DELAY_SEC)+" seconds")
        time.sleep(RECONNECTION_DELAY_SEC)
    
        try:
            OBDconnection = obd.OBD(port) 
        except:
            write_to_log("Unexpected error: "+str(sys.exc_info()[0]) )
    
        if n_reconnection_trials > RECONNECTION_MAX_TRIALS:
            write_to_log("Impossible to connect, quit application")
            quit()
    return OBDconnection
    
    
    
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

#time.sleep(1)
    
port = '/dev/rfcomm0'
#response = OBDconnection.query(obd.commands.ELM_VERSION); print(response)


OBDconnection = reconnect()
    

if OBDconnection.is_connected():
    nDatalines = 0
    
    init_LOG_FILEs()
    
    header = "Time"
    for cmd in cmds:
        header += LOG_SEP + cmd.name
    write_to_logData(header, LOGDATA_FILE, printTime = False)
    
    write_to_log("Connected to "+port)
    
    while True:
        logged_values = ""
        error_while_logging = False
        
        for cmd in cmds:
            response = OBDconnection.query(cmd)
            
            #logged_values += LOG_SEP + str(response.value.magnitude)
            try:
                logged_values += LOG_SEP + str(response.value.magnitude)
            except:
                error_while_logging = True
                write_to_log("Error in connection, reconnecting")
                OBDconnection = reconnect()
                
        if VERBOSE:
            print(logged_values)    
        
        #print(logged_values)
        
        if not error_while_logging:
            write_to_logData(logged_values, LOGDATA_FILE)

            nDatalines += 1
            if (nDatalines % 1000) == 0:
                write_to_log("Logged "+str(nDatalines)+" lines")

            #time.sleep(0.01)
        
        
    OBDconnection.close()
   
    LOGDATA_FILE.close()    
