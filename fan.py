
INDEFINITE = 5
import RPi.GPIO as GPIO

import wiringpi
import time
class Fan:
    def __init__(self):
        """
        Initialize code
        """

        
        # Setup PWM for DC Fan
        wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

        wiringpi.wiringPiSetupGpio()

        wiringpi.pinMode(18, 2)  # PWM output ONLY works on GPIO port 18

        wiringpi.pwmSetClock(6)  # this parameters correspond to 25 KHz
        wiringpi.pwmSetRange(128)


    def start_fan(self,pwm):
        """
        Args:
            pwm_value (int): value to run at
        
        Runs indefinitely
        """
        wiringpi.pwmWrite(18, pwm)  # maximum RPM
        time.sleep(INDEFINITE)

    def stop_fan(self):
        """
        Terminates fan
        """
        wiringpi.pwmWrite(18, 0)  # maximum RPM
        time.sleep(INDEFINITE)
