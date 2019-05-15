#!/usr/bin/python3
import obd
import time
import getpass
#import subprocess
import datetime
import sys
from threading import Thread

#sys.path.insert(0, '../')
#from config import cmds

# ELM327 v1.5
#subprocess.Popen("sudo rfcomm connect 0 00:0D:18:3A:67:89 1", shell=True)


## Logger management
#HOME_FOLDER             = '/home/pi'#+getpass.getuser()
LOG_FOLDER              = "/var/www/owncloud/data/raspi/files/logs/obd_logs/"
                            #HOME_FOLDER+"/Documents/logs/obd_logs/"
LOGDATA_FOLDER          = "/var/www/owncloud/data/raspi/files/logs/obddata_logs/"
                            #HOME_FOLDER+"/Documents/logs/obddata_logs/"
LOG_FILENAME            = "_obd.log"
LOGDATA_FILENAME        = "_obdData.log"
LOG_TOKEN               = "[O]"#"[USB_SHARE]"
LOG_SEP                 = ";"

PORT                    = '/dev/rfcomm0'

RECONNECTION_DELAY_SEC  = 10
RECONNECTION_MAX_TRIALS = 20

LOGDATA_FILE            = None
LOG_FILE                = None

VERBOSE                 = False

TS_S                    = 0.1 # sampling time
TIMEOUT_FOR_STOPLOG     = 60*5# s

n_reconnection_trials   = 1

cmds = [
    obd.commands.THROTTLE_POS,#
    obd.commands.SPEED, #
    obd.commands.RPM, #
    obd.commands.ENGINE_LOAD,# %
    obd.commands.FUEL_LEVEL,#
    obd.commands.COOLANT_TEMP,#
    #obd.commands.AMBIANT_AIR_TEMP,
    #obd.commands.INTAKE_PRESSURE,
    #obd.commands.INTAKE_TEMP,
    obd.commands.MAF,# gps
    #obd.commands.FUEL_RAIL_PRESSURE_DIRECT,
    #obd.commands.BAROMETRIC_PRESSURE,
    #obd.commands.CONTROL_MODULE_VOLTAGE,
    obd.commands.ACCELERATOR_POS_D,# % throttle
    #obd.commands.ACCELERATOR_POS_E,# % throttle
    #obd.commands.THROTTLE_ACTUATOR, # %
    obd.commands.OIL_TEMP,
    #'v': obd.commands.RELATIVE_THROTTLE_POS,#
    #obd.commands.ACCELERATOR_POS_F,
    #obd.commands.FUEL_RATE,
    #obd.commands.ABSOLUTE_LOAD,
    #obd.commands.COMMANDED_EQUIV_RATIO,
    #obd.commands.THROTTLE_POS_B,
    #obd.commands.THROTTLE_POS_C,
    #obd.commands.COMMANDED_EGR,
    #obd.commands.FUEL_RAIL_PRESSURE_VAC,
    #obd.commands.FUEL_PRESSURE,
    #obd.commands.TIMING_ADVANCE,
]
    
    
def write_to_log(msg):
    global LOG_FILENAME
    now = datetime.datetime.now()
    hms = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
    log_file = open(LOG_FOLDER+LOG_FILENAME, 'a')
    log_file.write(hms + " " + LOG_TOKEN + " " + msg + '\n')
    log_file.close() 

def write_to_logData(msg, logdata_file, printTime = True):
    #now = datetime.datetime.now()
    # hms = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
    millis = str(time.time())
    if printTime:
        logdata_file.write(millis + msg + '\n')
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
    
    
def OBDconnect(port, cmds):
    #OBDconnection = obd.OBD(port)
    OBDconnection = obd.Async(port)#, delay_cmds=0.05)
    for cmd in cmds:
        OBDconnection.watch(cmd) # keep track of the RPM
    OBDconnection.start()
    return OBDconnection
  
    
def OBDreconnect(port, cmds):
    OBDconnection = OBDconnect(port, cmds) 
    
    n_reconnection_trials = 0
    
    while not OBDconnection.is_connected():
        
        n_reconnection_trials += 1
        msg = str(n_reconnection_trials)+" Not connected, reconn. in "+str(RECONNECTION_DELAY_SEC)+" sec"
        write_to_log(msg)
        time.sleep(RECONNECTION_DELAY_SEC)
    
        try:
            OBDconnection = OBDconnect(port, cmds) 
        except:
            OBDconnection.stop()
            write_to_log("Unexpected error: "+str(sys.exc_info()[0]) )
    
        if n_reconnection_trials > RECONNECTION_MAX_TRIALS:
            OBDconnection.stop()
            write_to_log("Impossible to connect, quit application")
            quit()
    return OBDconnection
    
def threadSamplingTime(ts_s):
    time.sleep(ts_s)

#time.sleep(1)
#response = OBDconnection.query(obd.commands.ELM_VERSION); print(response)

write_to_log("Refresh OwnCloud index")
os.system("sudo -u www-data php  /var/www/owncloud/occ files:scan --all")



OBDconnection = OBDconnect(PORT, cmds)

t_init_for_stoplog  = time.time()
t_since_stop        = 0
nDatalines          = 0
engine_rpm          = 0
init_LOG_FILEs()

header = "Time_s"
for cmd in cmds: 
    header += LOG_SEP + cmd.name
write_to_logData(header, LOGDATA_FILE, printTime = False)

write_to_log("Connected to "+PORT)

while True:
    logged_values = ""
    error_while_logging = False
    logged_all_data = True
    
    ts_thread = Thread(target=threadSamplingTime, args=(TS_S,))
    ts_thread.start()
    
    for cmd in cmds:    
        try:
            response = OBDconnection.query(cmd)
            logged_values += LOG_SEP + str(response.value.magnitude)
            
            if cmd.name == 'RPM':
                engine_rpm  = response.value.magnitude
                
        except:
            write_to_log("Error when logging "+cmd.name)
            logged_all_data = False
            engine_rpm      = 0
            break
            
        #try:
        #    logged_values += LOG_SEP + str(response.value.magnitude)
        #except:
        #    error_while_logging = True
        #    write_to_log("Error in connection, reconnecting")
        #    OBDconnection.stop()
        #    OBDconnection = OBDreconnect(PORT, cmds)
              
    
    #print(logged_values)
    
    if logged_all_data: #not error_while_logging:
        if VERBOSE:
            print(logged_values)
        write_to_logData(logged_values, LOGDATA_FILE)

        nDatalines += 1
        if (nDatalines % 1000) == 0 :
            write_to_log("Logged "+str(nDatalines)+" lines")
    else:
        if VERBOSE:
            print("Error in logging")
        logged_values = ""
        
    #time.sleep(0.01)
    ts_thread.join()
    
    
    # if vehicle still, proceed to monitor whether stop the log
    if engine_rpm == 0:
        t_since_stop = time.time()-t_init_for_stoplog
    else:
        t_since_stop = 0
        t_init_for_stoplog = time.time()
        
    # stop the log
    if t_since_stop > TIMEOUT_FOR_STOPLOG:
        write_to_log("Engine RPM zero for "+str(TIMEOUT_FOR_STOPLOG)+" seconds, shutting down!")
        break
    
write_to_log("Closing OBD connection") 
OBDconnection.close()

write_to_log("Closing log data file") 
LOGDATA_FILE.close()    

write_to_log("Refresh OwnCloud index")
os.system("sudo -u www-data php  /var/www/owncloud/occ files:scan --all")

write_to_log("Exit") 

