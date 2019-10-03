
INDEFINITE = 1.5 #5 FIXME: 5 used for demo 1
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

        wiringpi.pwmSetClock(6)  # this parameters correspond to 25 KHz #192
        wiringpi.pwmSetRange(128) # 4096


    def start_fan(self,pwm):
        """
        Args:
            pwm_value (int): value to run at
        
        Runs indefinitely
        """
        wiringpi.pwmWrite(18, pwm)  # maximum RPM
        time.sleep(INDEFINITE)

    def update_fan(self,pwm):
        wiringpi.pwmWrite(18,pwm)

    def stop_fan(self):
        """
        Terminates fan
        """
        wiringpi.pwmWrite(18, 0)  # maximum RPM
        time.sleep(INDEFINITE)
