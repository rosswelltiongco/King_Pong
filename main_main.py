#importing modules
import RPi.GPIO as GPIO
import cv2   
import numpy as np
import os
import time
import serial

from lib.Base import*
from lib.Display import*
from lib.Camera import*
from lib.Sensor import*
#from lib.Solenoid import*

camera = Camera()
sensor = Sensor()
#ser = serial.Serial ("/dev/ttyS0", 57600 )    #Open port with baud rate

def main():
    while 1:
        #time.sleep(1)
        # Collect the center of the cup, in x axis
        # Collect the distance of the cup once aligned, in y axis
        midpoint = camera.scan_cups()
        distance = sensor.get_distance()
        #print("  y = ", distance)
        print("x = ", midpoint, "  y = ", distance)
        
        
        
        
    GPIO.cleanup(), 
main()








'''
        while True:
            ser.write(input('Enter'))                  #transmit data serially
            #Should print out "Bye!"
            #time.sleep(5)
            received_data = ser.read()              #read serial port
            time.sleep(1)
            data_left = ser.inWaiting()             #check for remaining byte
            received_data += ser.read(data_left)
            print (received_data)      
            time.sleep(0.1)
'''