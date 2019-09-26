#!/usr/bin/python3
# test operation of mcp3421 on i2c bus #1
import smbus
import os
import time
from ina219 import INA219
from fileLogger import fileLogger

class powerManagement(object):
    
    def __init__(self,
            file_logger_status  = fileLogger(),
            file_logger_data    = fileLogger(),
            debug               = False,
            verbose             = False,
            t_sleep_thrs_s      = 30,
            min_chrg_thrs_perc  = 15,
            batt_low_V          = 3.5,
            batt_high_V         = 4 ):
        
        # Power management config
        self.batt_low_V = batt_low_V
        self.batt_high_V = batt_high_V
        
        self.file_logger_status = file_logger_status;
        self.file_logger_data   = file_logger_data;
        
        self.debug              = debug
        self.min_chrg_thrs_perc = min_chrg_thrs_perc 
        self.t_sleep_thrs_s     = t_sleep_thrs_s
        
        log_sep = self.file_logger_data.log_sep
        if self.debug:
            header = 'Time_s'+log_sep+'usb_V'+log_sep+'batt_V'+log_sep+'batt_Vperc'+log_sep+'batt_Amp'+log_sep+'batt_Pow'
            self.file_logger_data.write_msg_to_log(header)
            self.t_sleep_thrs_s = 1
        
        self.__configMCP3421()
        self.__configina219()        
    
    def run(self):
        # main loop
        while True:
            time.sleep(self.t_sleep_thrs_s)
            
            # get data from mcp3421
            usb_V = self.__readV_mcp3421()
            # detect if the usb has been disconnected
            usb_is_connected = usb_V > 0.1
            
            res = __read_ina219()
            batt_V     = res[0] # Volts
            batt_Vperc = res[1] # %
            batt_Amp   = res[2] # Ampere
            batt_Pow   = res[3] # Watt
            
            # detect if battery is low
            battery_is_low  = batt_Vperc < self.min_chrg_thrs_perc
            
            # store the data
            if self.debug:
                log_sep = self.file_logger_data.log_sep
                msg = time.time()+log_sep+\
                      str(usb_V)+log_sep+\
                      str(batt_V)+log_sep+\
                      str(batt_Vperc)+log_sep+\
                      str(batt_Amp)+log_sep+\
                      str(batt_Pow)+log_sep
                self.file_logger_data.write_msg_to_log(msg)
            
            if battery_is_low and not usb_is_connected and not self.debug:
                break
                
        self.__close() # shut down if battery is low

    
    def __close(self):
        self.file_logger_status.write_msg_to_log('Battery low, shutting down')
        os.system('sudo shutdown -h now')
        
    def __configina219(self):
        # from https://raspi.tv/2017/how-much-power-does-pi-zero-w-use
        # we know that pizero at 5.2V (usb) consumes at max 300 mA (with margin), hence 1.6 W.
        # It means that at 3.7 V (battery) and 1.6 W, it absorbes 0.43 A > 0.5 A (with margin) 
        self.ina219 = ina219(shunt_ohms  = 0.1,
                         #max_expected_amps = 2, 
                         address           = 0x40)
        self.ina219.configure(voltage_range = self.ina219.RANGE_16V)#,
                          #gain          = ina219.GAIN_AUTO,
                          #bus_adc       = ina219.ADC_128SAMP,
                          #shunt_adc     = ina219.ADC_128SAMP)
        self.file_logger_status.write_msg_to_log("Configured ina219") 
        
                          
    def __configMCP3421(self):
        # Open i2c bus
        self.MCP3421_bus = smbus.SMBus(1)

        # i2C addresses and config
        deltasigUSB_mcp3421 = [0x68,0x69,0x6a,0x06b,0x6c,0x6d,0x6e,0x6f]           # device addresses
        self.MCP3421_addrUSB_mcp3421 = deltasigUSB_mcp3421[0]
        self.MCP3421_config_byte     = 0x1c # continuous mode, 18-bit resolution, gain = 1.
        self.MCP3421_bus.write_byte(
            self.MCP3421_addrUSB_mcp3421,
            self.MCP3421_config_byte) # configure the adc
        self.file_logger_status.write_msg_to_log("Configured MCP3421") 
    

    # NOTES:
    # * Tension divider with approx gain of VoltageDivider = 0.45 used to lower
    #   the input voltage from 3.7 V of the battery to +/-2.048 of the ADC.
    # * The ADC has 18 bit of resolution, hence 2^18 = 262144 counts correspond
    #   to a delta of 2*2.048 = 4.096. The gain of the ADC is therefore
    #   ADCgain = 4.096/262144 = 1.5625e-5 V/count
    # * When the battery is full, we have 3.7*0.45 = 1.665 V input to the ADC.
    #   This means, that when the battery is full we read
    #   (3.7*0.4545)/1.5625e-05 + (2^18/2) = 237632 counts
    # * Generalizing the above formula: ADCcounts = Vbatt*VoltageDivider/ADCgain + ADCoffset
    #   Which inverted give us: Vbatt = (ADCcounts - ADCoffset)*ADCgain/VoltageDivider
    def __readV_mcp3421(self):
        # ADC specific data, depend on hardware config
        ADCgain   = 4.096/262144
        ADCoffset = 0*2**18/2
        VoltageDivider = 100.0e3/(100e3+120e3+100e3)
        
        mcpdata = self.MCP3421_bus.read_i2c_block_data(
            self.MCP3421_addr_mcp3421,
            self.MCP3421_config_byte,
            4)
            
        conversionresults = mcpdata[2] + (mcpdata[1] << 8) + (mcpdata[0] << 16)
        
        conversionresults &= 0x1ffff     # lop off the sign ADC's sign extension
        if mcpdata[0] & 0x80:            # if the data was negative 
            conversionresults -= 0x20000     #     subtract off the sign extension bit
        
        USB_chrg_V = (conversionresults - ADCoffset)*ADCgain/VoltageDivider
        
        if self.debug:
            print('<mcp> conversion res. %f\tconfig-byte %s\tUSB_chrg_V %f' %
                (conversionresults, hex(mcpdata[3]), USB_chrg_V) )
                 
        return USB_chrg_V
    
    
    
    def __read_ina219(ina, DEBUG=False):        
        # read sensor
        #ina.wake()
        v = self.ina219.voltage()
        c = self.ina219.current()
        p = self.ina219.power()
        #ina.sleep()
        
        slope_perc = 100.0/(self.batt_high_V-self.batt_low_V)
        intercept_perc = 0 - slope_perc*self.batt_low_V
        
        vperc = slope_perc*v + intercept_perc
        vperc = round( max(min(vperc, 100), 0), 2)
        
        if self.debug:
            print('<ina> v %f\tvperc %f\tc %f\tp %f' % (v, vperc, c, p) )
        return [v, vperc, c, p]


if __name__ == '__main__':
    flogStatus = fileLogger(
        log_folder      = "/home/pi/Documents/logs/powmngm_logs/",
        log_filetoken   = "_powmngm.log",
        log_sep         = " ",
        log_token       = "[P]")

    flogData = fileLogger(
        log_folder      = "/home/pi/Documents/logs/powmngm_logs/",
        log_filetoken   = "_powmngmData.log",
        log_sep         = ";",
        log_token       = "")
    
                    
    usb = powerManagement(
        file_logger_status  = flogStatus,
        file_logger_data    = flogData,
        debug               = True,
        verbose             = True,
        t_sleep_thrs_s      = 30,
        min_chrg_thrs_perc  = 15,
        batt_low_V          = 3.5,
        batt_high_V         = 4 )
        
    usb.run