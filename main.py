import RPi.GPIO as GPIO
#from lib.Base import *
from lib.Solenoid import*
#from lib.Display import*
import time
import serial

#display = Display()
load = Solenoid(21)
shoot = Solenoid(19)
#base = Base()

ser = serial.Serial ("/dev/ttyS0", 57600 )    #Open port with baud rate

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

#def do_cup(cup):
    #pos = cups[cup][0]
    #base.go_to(pos)
    #if(cup <= 3 
    #launch()

def went_in(cup):
    go_in = raw_input("Did cup go in {0}? ".format(cup))
        
    if go_in == 'y':
        return True
    else:
        return False
    
    
def send_speed():
    ser.write(cup)                          #transmit data serially
    #Should print out "Bye!"
    #time.sleep(5)
    received_data = ser.read()              #read serial port
    time.sleep(1)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data)      
    time.sleep(0.1)
    
def main():    

    while 1:
        launch()
        """
        chosen_cup = int(input("Choose cup: "))
        do_cup(chosen_cup)
        
        while not went_in(chosen_cup):
            do_cup(chosen_cup)
        
        display.remove_cup(chosen_cup)
        display.display_cups()
        """
                    
       
    GPIO.cleanup()
    
main()
