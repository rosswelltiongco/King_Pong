#importing modules
import RPi.GPIO as GPIO
import cv2   
import numpy as np
import os
import time
import serial

from lib.Base import*
#from lib.Display import*
from lib.Solenoid import*
#from lib.Camera import*
#from lib.Sensor import*
load      = Solenoid(21)
shoot     = Solenoid(19)
INPUT_PIN = 36
GPIO.setup(INPUT_PIN, GPIO.IN)
#Port 8 : RX green PB0
#Port 10: TX yellow  PB1
#serial0 - ttyAMA0
#serial1 - ttyS0
os.system("sudo modprobe bcm2835-v4l2")
#camera = Camera()
#sensor = Sensor()
base    = Base()

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
cups = {0: [ 20,],
        1: [150,57],
        2: [260,57],
        3: [360,57],
        4: [ 85,54],
        5: [195,54],
        6: [310,54],
        7: [150,50],
        8: [260,50],
        9: [195,48]}

cups = {0: [bc-135 ,4],
        1: [bc-45  ,4],
        2: [bc+45  ,4],
        3: [bc+135 ,4],
        4: [bc-90  ,3],
        5: [bc     ,3],
        6: [bc+90  ,3],
        7: [bc-45  ,1],
        8: [bc+45  ,1],
        9: [bc     ,0]}
        distance = sensor.get_distance()
        #print("  y = ", distance)

        if GPIO.input(INPUT_PIN) == True:
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
bc = 197
base.step_left(bc)

cups = {0: [bc-180 ,4],
        1: [bc-45  ,4],
        2: [bc+45  ,4],
        3: [bc+135 ,4],
        4: [bc-90  ,3],
        5: [bc     ,3],
        6: [bc+90  ,3],
        7: [bc-45  ,1],
        8: [bc+45  ,1],
        9: [bc     ,0]}

def main():
    
    while 1:
        #bc = camera.scan()
        #load.block()
        temp = int(input())
        print(temp)
        #temp = str(cups[0][0]) # should be 4
        base.go_to(cups[temp][0])
        #print(temp)
        #ser.write(temp)  
        
        #temp = input('Enter: ')
        
        #ser.write(temp.encode())                  #transmit data serially

        #Should print out "Bye!"
        #while GPIO.input(INPUT_PIN) == False:
         #   print("waiting for TM4C")
        
        #time.sleep(1)
        # Collect the center of the cup, in x axis
        # Collect the distance of the cup once aligned, in y axis
        #time.sleep(0.5)
        #launch()
        #print("Done")

    GPIO.cleanup()
main()

