#!/usr/bin/python3
import datetime
import time

class fileLogger(Object):
    def __init__(self, log_folder, log_filetoken, log_sep, log_token):
        self.log_folder     = log_folder
        self.log_sep        = log_sep
        self.log_token      = log_token
        
        self.log_filename = self.__get_time_token()+log_filetoken
    
    def write_msg_to_log(self, msg):
        self.open_file()
        
        full_msg = hms+self.log_sep+self.log_token+self.log_sep+msg+'\n'
        self.file.write(full_msg)
        
        self.file.close()
    
    def open_file(self):
        self.file = open(self.log_folder + self.log_filename, 'a')
    
    def write_data_to_log(self, msg, printTime = True):
        millis = str(time.time())
        if printTime:
            self.file.write(millis + msg + '\n')
        else:
            self.file.write(msg + '\n')
            
    def __get_time_token(self):
        now = datetime.datetime.now()
        timenow = str(now)
        timenow = timenow.replace(' ', 'h')
        timenow = timenow.replace(':', '_')
        return timenow
        
        
    def close(self)
        self.file.close()