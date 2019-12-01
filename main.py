#importing modules
import RPi.GPIO as GPIO
import cv2   
import numpy as np
import os
import time
import serial

#from lib.Base import*
#from lib.Display import*
from lib.Solenoid import*
#from lib.Camera import*
#from lib.Sensor import*
load = Solenoid(21)
shoot = Solenoid(19)
BUTTON = 36
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

os.system("sudo modprobe bcm2835-v4l2")
#camera = Camera()
#sensor = Sensor()

ser = serial.Serial("/dev/ttyS0", 57600)    #Open port with baud rate


dist_0 = 48
dist_1 = 58
dist_2 = 64
dist_3 = 72
dist_4 = 80

def launch():
    # block off both solenoids
    load.block()
    shoot.block()
    time.sleep(2)
    load.block()
    # turn on fan
    #send_speed(cup)
    # allow for fan startup
    time.sleep(2)
    #load ball
    load.release()
    time.sleep(.03)
    # close load
    load.block()
    time.sleep(2)
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

"""
        distance = sensor.get_distance()
        #print("  y = ", distance)
        
        if (dist_0 < distance < dist_1):
            print("reference0")
        elif (dist_1 < distance < dist_2):
            print("reference1")
        elif (dist_2 < distance < dist_3):
            print("reference2")
        elif (dist_3 < distance < dist_4):
            print("reference3")
         
        push_button = GPIO.input(BUTTON)
        if push_button == True:
            print("Button pressed")
            #time.sleep(1)
            # Collect the center of the cup, in x axis
            # Collect the distance of the cup once aligned, in y axis
            time.sleep(0.5)
            launch()
            print("Done")
            #midpoint = camera.scan_cups()
            #distance = sensor.get_distance()
            #print("  y = ", distance)
            #print("x = ", midpoint, "  y = ", distance)
"""
def main():
    
    while 1:
        load.block()
        temp = input('Enter: ')
        
        ser.write(temp.encode())                  #transmit data serially
        #Should print out "Bye!"
        #time.sleep(10)
        
        #print("done. ready to launch")
        while GPIO.input(BUTTON) == False:
            pass
        print("Button pressed")
        #time.sleep(1)
        # Collect the center of the cup, in x axis
        # Collect the distance of the cup once aligned, in y axis
        time.sleep(0.5)
        launch()
        print("Done") 
            
    GPIO.cleanup()
main()

def shoot():
    push_button = GPIO.input(BUTTON)
    if push_button == True:
        print("Button pressed")
        #time.sleep(1)
        # Collect the center of the cup, in x axis
        # Collect the distance of the cup once aligned, in y axis
        time.sleep(0.5)
        launch()
        print("Done")

