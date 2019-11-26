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


def launch():
    # block off both solenoids
    load.block
    shoot.block()
    time.sleep(2)
    load.block()
    # turn on fan
    #send_speed(cup)
    # allow for fan startup
    time.sleep(2)
    #load ball
    load.release()
    time.sleep(.15)
    # close load
    load.block()
    time.sleep(1)
    # shoot ball
    shoot.release()
    time.sleep(2) # Follow through
    #close solenoid and turn fan off 
    shoot.block()
    
def went_in(cup):
    go_in = raw_input("Did cup go in {0}? ".format(cup))
        
    if go_in == 'y':
        return True
    else:
        return False

"""
#     cup:  pos,pwm
cups = {0: [ 20,57],
        1: [150,57],
        2: [260,57],
        3: [360,57],
        4: [ 85,54],
        5: [195,54],
        6: [310,54],
        7: [150,50],
        8: [260,50],
        9: [195,48]}
"""


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