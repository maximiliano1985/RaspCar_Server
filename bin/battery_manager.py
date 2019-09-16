#!/usr/bin/python3
# test operation of mcp3421 on i2c bus #1

import smbus
import os
import time
from ina219 import INA219

# General config
DEBUG = False

outfilename = '/home/pi/Documents/logs/'+str(round(time.time()))+'_adc_log.txt'

SLEEP_TIME_SECS = 30 # (s) measure the battery status every X seconds
if DEBUG:
    SLEEP_TIME_SECS = 1

MIN_CHARGE_PERC_THRESHOLD = 15 # below this, turn off the system


# Open i2c bus
bus = smbus.SMBus(1)

# i2C addresses and config
deltasigUSB_mcp3421 = [0x68,0x69,0x6a,0x06b,0x6c,0x6d,0x6e,0x6f]           # device addresses
addrUSB_mcp3421 = deltasigUSB_mcp3421[0]
config_byte = 0x1c          # continuous mode, 18-bit resolution, gain = 1.
bus.write_byte(addrUSB_mcp3421,config_byte) # configure the adc

SHUNT_OHMS = 0.1
# from https://raspi.tv/2017/how-much-power-does-pi-zero-w-use
# we know that pizero at 5.2V (usb) consumes at max 300 mA (with margin), hence 1.6 W.
# It means that at 3.7 V (battery) and 1.6 W, it absorbes 0.43 A > 0.5 A (with margin) 
MAX_EXPECTED_AMPS = 2
inaBATT = INA219(shunt_ohms         = SHUNT_OHMS,
                 #max_expected_amps  = MAX_EXPECTED_AMPS, 
                 address            = 0x40)
inaBATT.configure(voltage_range = inaBATT.RANGE_16V,
                  gain          = inaBATT.GAIN_AUTO,
                  bus_adc       = inaBATT.ADC_128SAMP,
                  shunt_adc     = inaBATT.ADC_128SAMP)
                  
# Init out file
fout = open(outfilename,'a')
fout.write('usb_V;batt_V;batt_Vperc;batt_Amp;batt_Pow\n')
fout.close()
    
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


def readV_mcp3421(bus, addr_mcp3421, config_byte, DEBUG=False):
    # ADC specific data, depend on hardware config
    ADCgain   = 4.096/262144
    ADCoffset = 0*2**18/2
    VoltageDivider = 100.0e3/(100e3+120e3+100e3)
    
    mcpdata = bus.read_i2c_block_data(addr_mcp3421,config_byte,4)
    conversionresults = mcpdata[2] + (mcpdata[1] << 8) + (mcpdata[0] << 16)
    
    conversionresults &= 0x1ffff     # lop off the sign ADC's sign extension
    if mcpdata[0] & 0x80:            # if the data was negative 
        conversionresults -= 0x20000     #     subtract off the sign extension bit
    
    USB_chrg_V = (conversionresults - ADCoffset)*ADCgain/VoltageDivider
    
    if DEBUG:
        print('<mcp> conversion res. %f\tconfig-byte %s\tUSB_chrg_V %f' %
            (conversionresults, hex(mcpdata[3]), USB_chrg_V) )
             
    return USB_chrg_V



def read_ina219(ina, DEBUG=False):
    # Power management config
    ZERO_VOLTAGE = 3.59
        
    # Battery specific data
    BATTERY_MAX_VOLTAGE = 3.7
    
    # read sensor
    ina.wake()
    v = ina.voltage()
    c = ina.current()
    p = ina.power()
    ina.sleep()
    
    slope_perc = 100.0/(BATTERY_MAX_VOLTAGE-ZERO_VOLTAGE)
    intercept_perc = 0 - slope_perc*ZERO_VOLTAGE
    
    vperc = slope_perc*v + intercept_perc
    vperc = round( max(min(vperc, 100), 0), 2)
    
    if DEBUG:
        print('<ina> v %f\tvperc %f\tc %f\tp %f' % (v, vperc, c, p) )
    
    return [v, vperc, c, p]


# main loop
while True:
    time.sleep(SLEEP_TIME_SECS)
    
    # get data from mcp3421
    usb_V = readV_mcp3421(bus, addrUSB_mcp3421, config_byte, DEBUG)
    # detect if the usb has been disconnected
    usb_is_connected = usb_V > 0.1
    
    res = read_ina219(inaBATT, DEBUG)
    batt_V     = res[0] # Volts
    batt_Vperc = res[1] # %
    batt_Amp   = res[2] # Ampere
    batt_Pow   = res[3] # Watt
    
    # detect if battery is low
    battery_is_low  = batt_Vperc < MIN_CHARGE_PERC_THRESHOLD

    # store the data
    fout = open(outfilename,'a')
    fout.write('%f;%f;%f;%f;%f\n'%(usb_V, batt_V, batt_Vperc, batt_Amp, batt_Pow))
    fout.close()
    
    if battery_is_low and not usb_is_connected and not DEBUG:
        fout = open(outfilename,'a')
        fout.write('Battery low, shutting down\n')
        fout.close()

        os.system('sudo shutdown -h now')
