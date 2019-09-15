
INDEFINITE = 5
import pigpio
from read_RPM import reader
import RPi.GPIO as GPIO


import wiringpi
import time

pi = pigpio.pi()

class Tach:
    def __init__(self):
        """
        Initialize code
        """
        # Setup GPIO for tach
        RPM_GPIO = 9
        tach = reader(pi, RPM_GPIO)
    
    def read_RPM(self):
        """
        Runs indefinitely
        """
        rpm = tach.RPM()
        print "RPM:"
        print rpm
        print " "
        time.sleep(2)

