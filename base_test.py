import RPi.GPIO as GPIO
from lib.Base import *
from lib.Solenoid import*
from lib.Fan import*
import time

fan = Fan()
solenoid = Solenoid()
base = Base(0)

def launch(pwm):    
    solenoid.block()
    fan.set_pwm(pwm)
    time.sleep(4)
    solenoid.release()
    time.sleep(2) # Follow through
    fan.set_pwm(0)

def main():
    """   
    [4] [3] [2] [1]
      [7] [6] [5]
        [9] [8]
          [10]
    """
    
    #     cup:  pos,pwm
    cups = {1 : [ 20,48],
            2 : [150,48],
            3 : [260,48],
            4 : [360,48],
            5 : [ 85,45],
            6 : [195,45],
            7 : [310,45],
            8 : [150,42],
            9 : [260,42],
            10: [195,40]}

    while 1:
        select = int(input("Enter cup"))
        pos = cups[select][0]
        base.go_to(pos)
        pwm = cups[select][1]
        launch(pwm)
                
    GPIO.cleanup()
main()