
INDEFINITE = 1.5 #5 FIXME: 5 used for demo 1
import RPi.GPIO as GPIO

import wiringpi
import time
class Switch:
    def __init__(self):
        """
        Initialize code
        """

               
        LimitSwitchUp = 22 # The limit switch is connected to this pin

        GPIO.setup(LimitSwitchUp, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)




    def switch_on(self):
        """
        Args:
            pwm_value (int): value to run at
        
        Runs indefinitely
        """


    def switch_off(self):


