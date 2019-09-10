
INDEFINITE = 5
import RPi.GPIO as GPIO

import wiringpi
import time
class Tach:
    def __init__(self):
        """
        Initialize code
        """
        # Setup GPIO for tach
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(21, GPIO.IN) # Port 21 = GPIO 9
    
    def read_rpm(self):
        """
        Args:
            pwm_value (int): value to run at
        
        Runs indefinitely
        """
        time.sleep(2)
        return rpm = tach.RPM()

    def display_rpm(self, rpm_value)
        """
        Args:
        rpm_value (int): value from tach
            
        Runs indefinitely
        """
        print "RPM: ", rpm_value

