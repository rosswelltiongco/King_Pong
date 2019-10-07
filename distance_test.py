"""
TODO ??: calib = 45 # Todo: Maybe use calibration for pwm_distance?
"""

import RPi.GPIO as GPIO
from lib.Fan import *
from lib.Solenoid import *
import time

fan = Fan()
solenoid = Solenoid()

def main():
    
    while 1:
        pwm_distances = [42, 45, 48, 51]
        selected_cup = int(input("Enter cup")) - 1
        pwm = pwm_distances[selected_cup]
        solenoid.block()
        fan.set_pwm(pwm)
        time.sleep(3)
        solenoid.release()
        time.sleep(1) # Follow through
        fan.set_pwm(0)
        
    GPIO.cleanup()

main()