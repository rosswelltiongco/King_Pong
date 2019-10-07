# Import for all
import RPi.GPIO as GPIO
import fan
import solenoid
import time
import wiringpi
import rpm
import PID
import base

wiringpi.wiringPiSetupGpio()
wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
        # Port for Soleniod
#GPIO.setup(19, GPIO.OUT)
        
LimitSwitchUp = 22 # The limit switch is connected to this pin

GPIO.setup(LimitSwitchUp, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)



maxDur = 150
curDur = 0
pollInterval = 0.001

one_cup   = 128
two_cup   = 256
three_cup = 384
off_set   = 64


def main():
    fan_obj = fan.Fan()
    #pid_obj = PID.PID()
    base_obj = base.Base()
    reset = False
    #solenoid_obj = solenoid.Solenoid()
    
    fan_obj.start_fan(64)
    print(rpm.get_rpm())
    time.sleep(3)
    fan_obj.stop_fan()
    
    """
    for x in range(1,4,1):
        flag = GPIO.input(LimitSwitchUp)
        solenoid_obj.block()
        time.sleep(5)
        
        if flag == 1:
            base_obj.stop_base(0)
            time.sleep(3)
            base_obj.move_left(384) #step all the way to align with leftmost cup
        elif flag == 0:
            base_obj.move_right(off_set)
            base_obj.stop_base(0)
            
            
            solenoid_obj.release()
            # Implement DC Dan
        
       
    while (reset == False):
        
        flag = GPIO.input(LimitSwitchUp)
        if flag == 1:
            base_obj.stop_base(0)
            time.sleep(3)
            base_obj.move_left(384) #step all the way to align with leftmost cup
        elif flag == 0:
            base_obj.move_right(64)
            base_obj.stop_base(0)
            reset = True
        
    
    time.sleep(3)
    
    
    while(1):
        flag = GPIO.input(LimitSwitchUp)
        if flag == 1:
            base_obj.stop_base()
            print "on"
            
            base_obj.move_left(100)
            base_obj.stop_base(0)
        elif flag == 0:
            print "off"
            base_obj.move_right(100)
            base_obj.stop_base()
        
            
        #time.sleep(1)
              
"""
    GPIO.cleanup()


main() # run main


