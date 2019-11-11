import RPi.GPIO as GPIO
from lib.Base import *
import time
import serial

GPIO.setmode(GPIO.BOARD)

TRIG = 40
ECHO = 38
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


class Sensor:
    def __init__(self):
        pass
            

            
    def get_distance(self):
        try:
            GPIO.output(TRIG, False)
            #print "Waiting For Sensor To Settle"
            time.sleep(3)
            
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
        
            while GPIO.input(ECHO)==0:
              pulse_start = time.time()

            while GPIO.input(ECHO)==1:
              pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration * 17150

            distance = round(distance, 2)
            
            return distance
        
        except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
            print("Cleaning up!")
            GPIO.cleanup()

sensor = Sensor()
sensor.get_distance()