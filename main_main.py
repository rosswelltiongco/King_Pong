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
ser = serial.Serial ("/dev/ttyS0", 57600 )    #Open port with baud rate

def main():
    while 1:
        time.sleep(1)
        midpoint = camera.scan_cups()
        distance = sensor.get_distance()
        
        print("x = ", midpoint, "  y = ", distance)
        
        
        while True:
            ser.write(raw_input("Enter"))                  #transmit data serially
            #Should print out "Bye!"
            #time.sleep(5)
            received_data = ser.read()              #read serial port
            time.sleep(1)
            data_left = ser.inWaiting()             #check for remaining byte
            received_data += ser.read(data_left)
            print (received_data)      
            time.sleep(0.1)
        
        
        
    GPIO.cleanup(), 
main()