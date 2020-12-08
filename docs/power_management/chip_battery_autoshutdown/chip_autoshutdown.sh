#!/bin/bash

# Forked https://github.com/xtacocorex/chip_batt_autoshutdown
# Modified to shutdown on microUSB unplug with code from
# https://bbs.nextthing.co/t/updated-battery-sh-dumps-limits-input-statuses/2921
# Service code from noimjosh https://github.com/noimjosh/chip_autoshutdown/
# MIT LICENSE, SEE LICENSE FILE

# LOGGING HAT-TIP TO http://urbanautomaton.com/blog/2014/09/09/redirecting-bash-script-output-to-syslog/

# SIMPLE SCRIPT TO POWER DOWN THE CHIP BASED UPON BATTERY VOLTAGE

# CHANGE THESE TO CUSTOMIZE THE SCRIPT
# ****************************
# ** THESE MUST BE INTEGERS **
CHARGE_LOW_LIMIT=20 # percentage of battery charge
MINCHARGECURRENT=10 # minimum ampere threshold

POLLING_WAIT=5m # time to wait between consecutive checks
#sleep .5 # Waits 0.5 second.
#sleep 5  # Waits 5 seconds.
#sleep 5s # Waits 5 seconds.
#sleep 5m # Waits 5 minutes.
#sleep 5h # Waits 5 hours.
#sleep 5d # Waits 5 days.

# ****************************

readonly SCRIPT_NAME=$(basename $0)
LAST_MESSAGE=""

log() {
    # echo "`date -u`" "$@"
    if [ "$@" != "$LAST_MESSAGE" ]; then
        LAST_MESSAGE="$@"
        logger -p user.notice -t "battery" "$@"
    fi
}

# TALK TO THE POWER MANAGEMENT
/usr/sbin/i2cset -y -f 0 0x34 0x82 0xC3



while true
do
    # GET POWER OP MODE
    POWER_OP_MODE=$(/usr/sbin/i2cget -y -f 0 0x34 0x01)

    CHARG_IND=$(($(($POWER_OP_MODE&0x40))/64))  # divide by 64 is like shifting rigth 6 times

    # SEE IF BATTERY EXISTS
    BAT_EXIST=$(($(($POWER_OP_MODE&0x20))/32))
    if [ $BAT_EXIST == 1 ]; then
        FUEL_GAUGE=$(/usr/sbin/i2cget -y -f 0 0x34 0x0b9)
        FUEL_GAUGE=$(($FUEL_GAUGE&0x7f))

            
        # CHECK BATTERY LEVEL AGAINST MINVOLTAGELEVEL
        if [ $FUEL_GAUGE -le $CHARGE_LOW_LIMIT ]; then
            log "CHIP BATTERY CHARGE IS LESS THAN $CHARGE_LOW_LIMIT"
            
            # GET THE CHARGE CURRENT
            BAT_ICHG_MSB=$(/usr/sbin/i2cget -y -f 0 0x34 0x7A)
            BAT_ICHG_LSB=$(/usr/sbin/i2cget -y -f 0 0x34 0x7B)
            BAT_ICHG_BIN=$(( $(($BAT_ICHG_MSB << 4)) | $(($(($BAT_ICHG_LSB & 0x0F)) )) ))
            BAT_ICHG_FLOAT=$(echo "($BAT_ICHG_BIN*0.5)"|bc)
            # CONVERT TO AN INTEGER
            BAT_ICHG=${BAT_ICHG_FLOAT%.*}
        
            # IF CHARGE CURRENT IS LESS THAN MINCHARGECURRENT, WE NEED TO SHUTDOWN
			if [ $CHARG_IND -eq 0 ]; then
            	if [ $BAT_ICHG -le $MINCHARGECURRENT ]; then
                	log "CHIP BATTERY IS NOT CHARGING, SHUTTING DOWN NOW"
                	shutdown -h now
				fi
            else
                log "CHIP BATTERY IS CHARGING"
            fi
        else
            #read Power OPERATING MODE register @01h
            #POWER_OP_MODE=$(/usr/sbin/i2cget -y -f 0 0x34 0x01)
            #echo $POWER_OP_MODE

            if [ $CHARG_IND -eq 1 ]; then
                log "BATTERY IS CHARGING"
            else
                BAT_IDISCHG_MSB=$(/usr/sbin/i2cget -y -f 0 0x34 0x7C)
                BAT_IDISCHG_LSB=$(/usr/sbin/i2cget -y -f 0 0x34 0x7D)
                BAT_IDISCHG_BIN=$(( $(($BAT_IDISCHG_MSB << 5)) | $(($(($BAT_IDISCHG_LSB & 0x1F)) )) ))
                BAT_IDISCHG=$(echo "($BAT_IDISCHG_BIN)"|bc)
                if [ $BAT_IDISCHG -le $MINCHARGECURRENT ]; then
                    log "BATTERY IS CHARGED"
                else
                    log "BATTERY DISCHARGING"
                fi 
            fi
            # log "CHIP BATTERY LEVEL IS GOOD"
        fi
    else
        log "BATTERY NOT PRESENT."
    fi
    sleep $POLLING_WAIT
done
