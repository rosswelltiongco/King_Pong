#!/usr/bin/python -u
# tachfan.py - read RPM from a PC fan tachometer wired to GPIO
#
# references:
# http://electronics.stackexchange.com/questions/8295/how-to-interpret-the-output-of-a-3-pin-computer-fan-speed-sensor
# http://www.formfactors.org/developer/specs/REV1_2_Public.pdf

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TACH = 3 # BCM 16

GPIO.setwarnings(False)
GPIO.setup(TACH, GPIO.IN, pull_up_down=GPIO.PUD_UP)


values = []


t = time.time()
def fell(n):
    global t
    dt = time.time() - t
    # if dt < 0.01: return # reject spuriously short pulses

    freq = 1 / dt
    rpm = (freq / 2) * 60
    
    # Remove outliers
    if rpm > 25000:
        return
    
    
    
    # Accumulate a running average
    if len(values) < 10:
        values.append(rpm)
    else:
        values.pop(0)
        values.append(rpm)
    # print "%.f" % (rpm,)
    
    t = time.time() 

def get_rpm():
    avg_pwm = int(sum(values)/10) #FIXME: len(values)?
    return "%.f" % (avg_pwm,) 

GPIO.add_event_detect(TACH, GPIO.FALLING, fell)

# while True: time.sleep(1e9)

#while 1:   print(get_rpm())