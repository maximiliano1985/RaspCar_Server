#!/usr/bin/python3
# test operation of mcp3421 on i2c bus #1

import smbus
import time

DEBUG = 1

# battery specific data
ADCgain   = 4.096/262144
ADCoffset = 0*2**18/2
VoltageDivider = 100.0e3/(100e3+120e3)
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

if DEBUG:
    fout = open('adc_log.txt', 'w')

while True:
    time.sleep(1)
    mcpdata = bus.read_i2c_block_data(deltasig[0],config_byte,4)
    conversionresults = mcpdata[2] + (mcpdata[1] << 8) + (mcpdata[0] << 16)
    print('Conversion results =',(conversionresults), 'config-byte:',hex(mcpdata[3]))

    conversionresults &= 0x1ffff     # lop off the sign ADC's sign extension
    if mcpdata[0] & 0x80:            # if the data was negative 
        conversionresults -= 0x20000     #     subtract off the sign extension bit

    batt_chrg_V = (conversionresults - ADCoffset)*ADCgain/VoltageDivider
    #print('Conversion results =',hex(conversionresults), 'config-byte:',hex(mcpdata[3]))
    print('Raw:',(conversionresults),'- Cooked: %.3f' % batt_chrg_V,'\bV',
          '- config-byte:',hex(mcpdata[3]))

    if DEBUG:
        fout.write('%f\n'%batt_chrg_V)



if DEBUG:
    fout.close()
