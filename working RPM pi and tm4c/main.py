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
from lib.Camera import*
#from lib.Sensor import*
load      = Solenoid(21)
shoot     = Solenoid(19)
load.block()
shoot.block()
INPUT_PIN = 36
GPIO.setup(INPUT_PIN, GPIO.IN)
#Port 8 : RX green PB0
#Port 10: TX yellow  PB1
#serial0 - ttyAMA0
#serial1 - ttyS0
os.system("sudo modprobe bcm2835-v4l2")
base    = Base()
base.step_left(197)

camera = Camera(base)

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
    time.sleep(.1)
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

"""


def main():
    bc = camera.scan_cups()
    base.set_pos(bc)
    #bc =0
    cups = {0: [bc-170 ,3],
            1: [bc-45  ,3],
            2: [bc+45  ,3],
            3: [bc+135 ,3],
            4: [bc-90  ,2],
            5: [bc     ,2],
            6: [bc+90  ,2],
            7: [bc-45  ,1],
            8: [bc+45  ,1],
            9: [bc     ,0]}
    
    print(base.get_pos)
    
    while 1:
        
        load.block()
        
        temp = int(input('Enter: '))
        base.go_to(cups[temp][0])
        time.sleep(2)
        signal = str(cups[temp][1]) # should be 4
        
        #ser.write(temp)  
        
        #temp = input('Enter: ')
        
        
        ser.write(signal.encode())#.encode())                  #transmit data serially
        #time.sleep(.5)
        #Should print out "Bye!"
        while GPIO.input(INPUT_PIN) == False:
            print("waiting for TM4C")
            #time.sleep(2)
        
        #Collect the center of the cup, in x axis
        #Collect the distance of the cup once aligned, in y axis
        time.sleep(0.5)
        launch()
        print("Done")
        
    GPIO.cleanup()
main()

