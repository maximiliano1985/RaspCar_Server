#!/usr/bin/python3
# test operation of mcp3421 on i2c bus #1

import smbus
import os
import time

DEBUG = 0

outfilename = '/home/pi/Documents/logs/'+str(round(time.time()))+'_adc_log.txt'

ZERO_VOLTAGE = 3.59
MIN_CHARGE_PERC_THRESHOLD = 15 # below this, turn off the system

SLEEP_TIME_SECS = 30 # (s) measure the battery status every X seconds

# Battery specific data
BATTERY_MAX_VOLTAGE = 3.7
slope_perc = 100.0/(BATTERY_MAX_VOLTAGE-ZERO_VOLTAGE)
intercept_perc = 0 - slope_perc*ZERO_VOLTAGE

# ADC specific data
ADCgain   = 4.096/262144
ADCoffset = 0*2**18/2
VoltageDivider = 100.0e3/(100e3+120e3)

VoltageDividerUSB = 100.0e3/(100e3+100e3+120e3)

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

deltasig = [0x68,0x69,0x6a,0x06b,0x6c,0x6d,0x6e,0x6f]           # device addresses
config_byte = 0x1c          # continuous mode, 18-bit resolution, gain = 1.

bus = smbus.SMBus(1)
bus.write_byte(deltasig[0],config_byte) # configure the adc

while True:
    time.sleep(SLEEP_TIME_SECS)
    mcpdata = bus.read_i2c_block_data(deltasig[0],config_byte,4)
    conversionresults = mcpdata[2] + (mcpdata[1] << 8) + (mcpdata[0] << 16)
    print('Conversion results =',(conversionresults), 'config-byte:',hex(mcpdata[3]))

    conversionresults &= 0x1ffff     # lop off the sign ADC's sign extension
    if mcpdata[0] & 0x80:            # if the data was negative 
        conversionresults -= 0x20000     #     subtract off the sign extension bit

    batt_chrg_V = (conversionresults - ADCoffset)*ADCgain/VoltageDivider
    
    batt_chrg_perc = slope_perc*batt_chrg_V + intercept_perc
    batt_chrg_perc = round( max(min(batt_chrg_perc, 100), 0), 2)
    
    #print('Conversion results =',hex(conversionresults), 'config-byte:',hex(mcpdata[3]))
    print('Raw:',(conversionresults),'- Cooked: %.3f' % batt_chrg_V,'\bV',
          ' (%.2f) '% batt_chrg_perc,'\b%',
          '- config-byte:',hex(mcpdata[3]) )

    fout = open(outfilename,'a')
    fout.write('%f\n'%batt_chrg_perc)
    fout.close()

    low_battery      = batt_chrg_perc < MIN_CHARGE_PERC_THRESHOLD
    charging_battery = False ### EDIT THIS AFTER A MULTIPLEXER IS USED TO MONITOR THE POWERBOOST 1000C
    if low_battery and not charging_battery:
        fout = open(outfilename,'a')
        fout.write('Battery low, shuting down\n')
        fout.close()

        os.system('sudo shutdown -h now')
