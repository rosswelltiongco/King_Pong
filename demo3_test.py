
import RPi.GPIO as GPIO
from lib.Fan import *
from lib.Base import *
import base_test
from lib.Solenoid import *
import time

solenoid_obj = Solenoid()
fan = Fan()

def main():
    print "me"
    base_obj = base_test.Base(0)
    base_obj.move_left(2)
    solenoid_obj.block()
    time.sleep(1)
    solenoid_obj.release()
    
    
    while 1:
        pwm_distances = [42, 45, 48, 51]
        base_distances = [128, 128, 128, 128]
        selected_cup = int(input("Enter cup")) - 1
        
        if (selected_cup == 1):
        
        
            
            pwm = pwm_distances[selected_cup]
            solenoid_obj.block()
            fan.set_pwm(pwm)
            time.sleep(3)
            solenoid_obj.release()
            time.sleep(1) # Follow through
            fan.set_pwm(0)
        elif (selected_cup == 2):
        
        
            base_obj.move_left(128)
            pwm = pwm_distances[selected_cup]
            solenoid_obj.block()
            fan.set_pwm(pwm)
            time.sleep(3)
            solenoid_obj.release()
            time.sleep(1) # Follow through
            fan.set_pwm(0)
        
        else:
            pass
    GPIO.cleanup()


main()

