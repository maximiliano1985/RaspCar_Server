#!/usr/bin/python3
import obd
import time
#import subprocess
import sys
import signal
from threading import Thread
from fileLogger import fileLogger

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

#sys.path.insert(0, '../')
#from config import CMDS

# ELM327 v1.5
#subprocess.Popen("sudo rfcomm connect 0 00:0D:18:3A:67:89 1", shell=True)

CMDS = [
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

class obdRecorder(object):
    
    def __init__(self, port     = '/dev/rfcomm0',
                reconnect_delay_sec     = 10,
                reconnect_max_trials    = 20,
                file_logger_status      = fileLogger(),
                file_logger_data        = fileLogger(),
                log_to_file             = True):
        
        self.port                    = port
        self.reconnect_max_trials    = reconnect_max_trials
        self.n_reconnect_trials      = 1
        
        self.file_logger_status = file_logger_status;
        self.file_logger_data   = file_logger_data;
        self.log_to_file        = log_to_file
                
        self.log_sep = ';'
        
    def init_log_data_file(self):
        
        self.header = "Time_s"
        for cmd in CMDS:
            self.header += ';' + cmd.name
            
        if self.log_to_file == True:
            self.file_logger_data.open_file()
            self.file_logger_data.write_data_to_log(self.header, printTime = False)
                
                
    def connect(self):
        #OBDconnection = cm
        self.OBDconnection = obd.Async(self.port)#, delay_CMDS=0.05)
        
        if self.OBDconnection.is_connected():
            if self.log_to_file:
                self.file_logger_status.write_msg_to_log("Connected to "+self.port)
            
            for cmd in CMDS:
                self.OBDconnection.watch(cmd) # keep track of the RPM
            
            if self.log_to_file:
                self.file_logger_status.write_msg_to_log("Watching requested commands")
            
            
            self.init_log_data_file()
            self.OBDconnection.start()
            return True
        else:
            return False
          
    def close(self):
        if self.log_to_file:
            self.file_logger_status.write_msg_to_log("Closing OBD connection") 
        self.OBDconnection.close()

        if self.log_to_file:
            self.file_logger_status.write_msg_to_log("Closing log data file") 
            self.file_logger_data.close()    

            self.file_logger_status.write_msg_to_log("Exit")        
        
    def reconnect(self):
        self.n_reconnect_trials = 0
    
        while not self.OBDconnection.is_connected():
            time.sleep(self.reconnect_max_trials)
            
            self.n_reconnect_trials += 1
            if self.log_to_file:
                msg = str(self.n_reconnect_trials)+" Not connected, reconn. in "+str(self.reconnect_max_trials)+" sec"
                self.file_logger_status.write_msg_to_log(msg)
    
            try:
                return self.OBDconnect()
            except:
                self.OBDconnection.stop()
                if self.log_to_file:
                    self.file_logger_status.write_msg_to_log("Unexpected error: "+str(sys.exc_info()[0]) )
                return False
                
            if self.n_reconnect_trials > self.reconnect_max_trials:
                self.OBDconnection.stop()
                if self.log_to_file:
                    self.file_logger_status.write_msg_to_log("Impossible to connect, quit application")
                quit()
                return False
    
    
    def read_once(self):
            
        logged_values   = "" # output string
        logged_all_data = True
        engine_rpm      = 0
        for cmd in CMDS:    
            try:
                response = self.OBDconnection.query(cmd)
                logged_values += self.log_sep + str(response.value.magnitude)
        
                if cmd.name == 'RPM':
                    engine_rpm  = response.value.magnitude
            except:
                if self.log_to_file:
                    self.file_logger_status.write_msg_to_log("Error when logging "+cmd.name)
                logged_all_data = False
                engine_rpm      = 0
                break 
                
        return logged_all_data, logged_values, engine_rpm
                
                
    def read(self, sampling_time_s, verbose = False):
        nDatalines      = 0
        while True:    
            ts_thread = Thread(target=time.sleep(sampling_time_s))
            ts_thread.start()
    
            logged_all_data, logged_values, engine_rpm = self.read_once()
    
            if logged_all_data: # not error_while_logging:
                if verbose:
                    print(logged_values)
                if self.log_to_file:
                    self.file_logger_data.write_data_to_log(logged_values)

                nDatalines += 1
                if (nDatalines % 1000) == 0 and self.log_to_file:
                    self.file_logger_status.write_msg_to_log("Logged "+str(nDatalines)+" lines")
                    nDatalines = 0
            else:
                if verbose:
                    print("Error in logging")
                break
        
            #time.sleep(0.01)
            ts_thread.join()
          


if __name__ == '__main__':
    #self.file_logger_status.write_msg_to_log("Refresh OwnCloud index")
    #os.system("sudo -u www-data php  /var/www/owncloud/occ files:scan --all")
    
    ## Logger management
    flogStatus = fileLogger(
        log_folder      = "/home/pi/Documents/logs/obd_logs/",
        log_filetoken   = "_obd.log",
        log_sep         = " ",
        log_token       = "[O]")

    flogData = fileLogger(
        log_folder      = "/home/pi/Documents/logs/obddata_logs/",
        log_filetoken   = "_obdData.log",
        log_sep         = ";",
        log_token       = "")
    
    rec = obdRecorder(port     = '/dev/rfcomm0',
                reconnect_delay_sec     = 10,
                reconnect_max_trials    = 20,
                file_logger_status      = flogStatus,
                file_logger_data        = flogData,
                log_to_file             = False)
    rec.connect()
    rec.read( sampling_time_s = 0.1, verbose = False)
    
    rec.close()
