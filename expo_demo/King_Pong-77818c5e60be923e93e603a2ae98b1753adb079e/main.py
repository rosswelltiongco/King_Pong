import RPi.GPIO as GPIO
from lib.Base import *
from lib.Solenoid import*
from lib.Fan import*
from lib.Display import*
from lib.Camera import*
import time

display = Display()
fan = Fan()
solenoid = Solenoid()
camera = Camera()
base = Base()

load      = Solenoid(21)
shoot     = Solenoid(19)

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
#     cup:  pos,pwm
cups = {0: [ 20,48],
        1: [150,48],
        2: [260,48],
        3: [360,48],
        4: [ 85,45],
        5: [195,45],
        6: [310,45],
        7: [150,42],
        8: [260,42],
        9: [195,40]}
"""
def launch(pwm):    
    solenoid.block()
    fan.set_pwm(pwm)
    time.sleep(4)
    solenoid.release()
    time.sleep(2) # Follow through
    fan.set_pwm(0)

def reload():
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




def do_cup(cup):
    pos = cups[cup][0]
    base.go_to(pos)
    pwm = cups[cup][1]
    launch(pwm)

def went_in(cup):
    go_in = raw_input("Did cup go in {0}? ".format(cup))
        
    if go_in == 'y':
        return True
    else:
        return False
    
def main():    

    while 1:
        chosen_cup = int(input("Choose cup: "))
        do_cup(chosen_cup)
        
        while not went_in(chosen_cup):
            do_cup(chosen_cup)
        
        display.remove_cup(chosen_cup)
        display.display_cups()
                    
       
    GPIO.cleanup()
    
main()
