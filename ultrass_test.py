import RPi.GPIO as GPIO
from lib.Base import *
#from lib.Solenoid import*
#from lib.Display import*
import time
import serial


#display = Display()
#load = Solenoid(21)
#shoot = Solenoid(19)
base = Base()
GPIO.setmode(GPIO.BOARD)


cup = {0: [20],
        1: [150],
        2: [260],
        3: [360],
        4: [85],
        5: [195],
        6: [310],
        7: [150],
        8: [260],
        9: [195],}

scan_cup = {0: [5],
            1: [70],
            2: [145],
            3: [210],
            4: [300],
            5: [345],
            6: [405]}

xx = [60, 50, 40, 30, 40, 50, 60]
y = [0,  1,   2,  3,  4,  5,  6]

TRIG = 40
ECHO = 38

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

dist = []

def graph(x, y):
    import matplotlib.pyplot as plt
    
    plt.plot(x, y, 'ro')
    plt.xlabel('Cup')
    plt.ylabel('Distance')
    plt.xlim([0, 7])
    plt.ylim([0, 50])
    plt.show()


time.sleep(1)

try:
    #while True:

    for x in range(0,7):
        base.go_to(scan_cup[x][0])
        time.sleep(1)
        GPIO.output(TRIG, False)
        #print "Waiting For Sensor To Settle"
        time.sleep(3)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
    
        while GPIO.input(ECHO)==0:
          pulse_start = time.time()

        while GPIO.input(ECHO)==1:
          pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)
        
        dist.append(distance)

        print ("Distance:",distance,"cm")
            
    print( "Array:", dist)

except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    GPIO.cleanup()



graph(y, dist)