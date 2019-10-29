'''
UART communication on Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial
from time import sleep

"""
ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
while True:
    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data)                   #print received data
    ser.write(received_data)                #transmit data serially
'''
    
    
ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
while True:
    ser.write("rnSay something:")           #transmit data serially
    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data)                   #print received data
    ser.write("rnSay something:" + recieved_data) #transmit data serially
"""

port = serial.Serial ("/dev/ttyAMA0", 9600)
while True:
        yes = port.readline()
        print(yes)           #read serial port