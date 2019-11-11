#importing modules
import RPi.GPIO as GPIO
import cv2   
import numpy as np
import os
from lib.Base import *
#from lib.Solenoid import*
from lib.Display import*
from lib.Camera import*
from lib.Sensor import*
import time
import serial

camera = Camera()
sensor = Sensor()

def main():
    while 1:
        time.sleep(1)
        midpoint = camera.scan_cups()
        distance = sensor.get_distance()
        
        print("x = ", midpoint, "  y = ", distance)
        
        
    GPIO.cleanup(), 
main()