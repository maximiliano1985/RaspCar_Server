import RPi.GPIO as GPIO

LED_BLUE    = 33
LED_GREEN   = 35
LED_RED     = 37


GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(LED_BLUE, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(LED_GREEN, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(LED_RED, GPIO.OUT, initial=GPIO.LOW) 


def set_led(red_on = False, blue_on = False, green_on = False):
    if red_on:
        GPIO.output(LED_RED     , GPIO.HIGH)
    else:
        GPIO.output(LED_RED     , GPIO.LOW)

    if green_on:
        GPIO.output(LED_GREEN     , GPIO.HIGH)
    else:
        GPIO.output(LED_GREEN     , GPIO.LOW)
        
    if blue_on:
        GPIO.output(LED_BLUE     , GPIO.HIGH)
    else:
        GPIO.output(LED_BLUE     , GPIO.LOW)