'''
The Pi will send the desired RPM and recieve flag to launch the ball
'''
import serial
from time import sleep

ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
while True:
    ser.write("Hello!")                     #transmit data serially
    # Should print out "Bye!"
    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data)                   #print received data
