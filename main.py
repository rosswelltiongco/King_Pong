import RPi.GPIO as GPIO
from lib.Base import *
from lib.Solenoid import*
from lib.Fan import*
from lib.Display import*
import time

display = Display()
fan = Fan()
solenoid = Solenoid()
base = Base()

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

def launch(pwm):    
    solenoid.block()
    fan.set_pwm(pwm)
    time.sleep(4)
    solenoid.release()
    time.sleep(2) # Follow through
    fan.set_pwm(0)

def do_cup(cup):
    pos = cups[cup][0]
    base.go_to(pos)
    pwm = cups[cup][1]
    launch(pwm)

def went_in(cup):
    go_in = raw_input("Did cup go in {0}".format(cup))
    """
    while go_in != 'y':
        go_in = raw_input("Did cup go in {0}".format(cup))
    """
    
    if go_in == 'y':
        return True
    else:
        return False
    
def main():    

    while 1:
        chosen_cup = int(input("Choose cup"))
        do_cup(chosen_cup)
        
        while not went_in(chosen_cup):
            do_cup(chosen_cup)
        
        display.remove_cup(chosen_cup)
        display.display_cups()
                    
       
    GPIO.cleanup()
    
main()
