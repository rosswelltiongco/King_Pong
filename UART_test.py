'''
The Pi will send the desired RPM and recieve flag to launch the ball
'''

import RPi.GPIO as GPIO

import serial
from time import sleep
import time

#Port 8 : RX
#Port 10: TX
#serial0 - ttyAMA0
#serial1 - ttyS0

ser = serial.Serial("/dev/ttyS0", 57600)    #Open port with baud rate
    
while True:
    ser.write(raw_input('enter'))                  #transmit data serially
    #Should print out "Bye!"
    #time.sleep(2)
    #print("here")
    """
    received_data = ser.read()              #read serial port
    time.sleep(1)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data)
    time.sleep(0.1)
    """
    time.sleep(0.5)
    received_data = ser.read()
    print (received_data)
    time.sleep(0.5)
    if received_data == '1':
        print("Cup 1")
    elif received_data == '2':
        print("Cup 2")
    elif received_data == '3':
        print("Cup 3")
    elif received_data == '4':
        print("Cup 4")
    else:
        print("nothing")
    
    