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
GPIO.setup(19, GPIO.OUT)

def main():
    fan_obj = fan.Fan()
    pid_obj = PID.PID()
    base_obj = base.Base()
    
    #solenoid_obj = solenoid.Solenoid()
    fan_obj.start_fan(64)
    #base_obj.move_right(64) # 128 = 1 cup difference. 64 = 1/2 offset
    """
    
    quit = False
    print "Welcome to Demo 2 of King Pong!\n"
    print "Loading -____-"
    fan_obj.stop_fan()
    
    
    
    while(quit==False):
        solenoid_obj.release()
        print "Please wait for fan..."
    
    fan_obj.start_fan(64)
    while(1):
        # time.sleep(0.5)
        # Initalize sp and collect rpm(4 figures)
        pid_obj.setPoint(15000)
        time.sleep(1)
        pv = int(pid_obj.update(int(rpm.get_rpm())))
        time.sleep(1)
        print("RPM: {0}    PV: {1}".format(int(rpm.get_rpm()),pv))
        #print("rpm ", int(rpm.get_rpm()))
        #print ("pv: " ,pv)
        fan_obj.start_fan(pv+64)
        #print("PWM: {0}\nRPM: {1}\nPV: {2}".format(pv,int(rpm.get_rpm()),pv))
    
    """
    
    

    GPIO.cleanup()


main() # run main

