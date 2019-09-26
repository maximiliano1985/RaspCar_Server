import time
from threading import Thread

from fileLogger import fileLogger
from gpsRecorder import gpsRecorder
from obdRecorder import obdRecorder

class dataRecorder(object):
    def __init__(self,
            gps                 = gpsRecorder(),
            obd                 = obdRecorder(),
            file_logger_status  = fileLogger(),
            file_logger_data    = fileLogger() ):
            
        self.gps = gps
        self.obd = obd
        
        self.file_logger_status = file_logger_status
        self.file_logger_data   = file_logger_data
        self.file_logger_data.open_file()
        
        obd.connect()
        self.file_logger_status.write_msg_to_log("Connected OBD to port: "+self.obd.port)
        
        
        header = self.obd.header+self.gps.header
        self.file_logger_data.write_data_to_log(header, printTime = False)
    
    def close(self):
        self.obd.close()
        self.file_logger_status.write_msg_to_log("Closed OBD connection") 
        
        self.file_logger_data.close()
        self.file_logger_status.write_msg_to_log("Closed data log") 
        
        
    def run(self, sampling_time_s, verbose= False, timeout_stoplog = 60*5):
        t_since_moving  = time.time()
        t_since_stop    = 0
        nDatalines      = 0
        engine_rpm      = 0
        log_sep         = self.file_logger_data.log_sep
        
        logged_gps_old = ['0','0','0','0','0','0','0','0','0']
        while True:    
            ts_thread = Thread( target=time.sleep(sampling_time_s) )
            ts_thread.start()
            
            # Log the OBD
            logged_all_data, logged_obd_values, engine_rpm = self.obd.read_once()
    
            if logged_all_data: # not error_while_logging:
                
                # log the gps
                logged_gps_ary = self.gps.read_once()
                # manage gps data in case of error
                if logged_gps_ary[1] == 'E':
                    logged_gps_ary = logged_gps_old
                else:
                    logged_gps_old = logged_gps_ary
                    
                logged_gps_values = ""
                for datastr in logged_gps_ary:
                    logged_gps_values += log_sep + datastr
                logged_all_data = logged_obd_values + logged_gps_values
                
                if verbose:
                    print(logged_all_data)
                    
                self.file_logger_data.write_data_to_log( logged_all_data )
                
            
                nDatalines += 1
                if (nDatalines % 1000) == 0 and self.log_to_file:
                    self.file_logger_status.write_msg_to_log("Logged "+str(nDatalines)+" lines")
                    nDatalines = 0
            else:
                if verbose:
                    print("Error in logging OBD data")
                break
        
            #time.sleep(0.01)
            ts_thread.join()
    
    
            # if vehicle still, proceed to monitor whether stop the log
            if engine_rpm == 0:
                t_since_stop = time.time()-t_since_moving
            else:
                t_since_stop = 0
                t_since_moving = time.time()
        
            # stop the log
            if t_since_stop > timeout_stoplog:
                msg = "Engine RPM zero for "+str(timeout_stoplog)+" seconds, stop recorder"
                self.file_logger_status.write_msg_to_log(msg)
                break
                
        
            
if __name__ == '__main__':
    
    gpsRec = gpsRecorder(port='/dev/ttyS0', baudrate = 19200, debug = True)
    
    obdRec = obdRecorder(port     = '/dev/rfcomm0',
                reconnect_delay_sec     = 10,
                reconnect_max_trials    = 20,
                log_to_file             = False)
    
    flogStatus = fileLogger(
        log_folder      = "/home/pi/Documents/logs/recorder_logs/",
        log_filetoken   = "_rec.log",
        log_sep         = " ",
        log_token       = "[R]")
    flogData = fileLogger(
        log_folder      = "/home/pi/Documents/logs/recorderdata_logs/",
        log_filetoken   = "_obdData.log",
        log_sep         = ";",
        log_token       = "")
            
    rec = dataRecorder(
        gps                 = gpsRec,
        obd                 = obdRec,
        file_logger_status  = flogStatus,
        file_logger_data    = flogData
    )
    res.run(0.1, verbose= True, timeout_stoplog = 60*5)