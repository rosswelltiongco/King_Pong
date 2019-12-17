'''
The Pi will send the desired RPM and recieve flag to launch the ball
'''

import RPi.GPIO as GPIO

import serial
from time import sleep
import time

#Port 8 : RX green PB0
#Port 10: TX yellow  PB1
#serial0 - ttyAMA0
#serial1 - ttyS0

ser = serial.Serial("/dev/ttyS0", 57600)    #Open port with baud rate
    
while True:
    temp = input('Enter: ')
    ser.write(temp.encode())                  #transmit data serially
    #Should print out "Bye!"
    time.sleep(15)
    
    #print("here")
    received_data = ser.read()              #read serial port
    """
    time.sleep(1)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data)
    time.sleep(0.1)
    time.sleep(.5)
    received_data = ser.read()
    """
    print (received_data)
    time.sleep(0.1)