# Import for all
import RPi.GPIO as GPIO
import fan
import solenoid
import time
import wiringpi
import rpm
import PID

wiringpi.wiringPiSetupGpio()
wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
        # Port for Soleniod
GPIO.setup(19, GPIO.OUT)

def main():
    fan_obj = fan.Fan()
    pid_obj = PID.PID()
    
    solenoid_obj = solenoid.Solenoid()
    quit = False
    print "Welcome to Demo 2 of King Pong!\n"
    print "Loading -____-"
    fan_obj.stop_fan()
    
    while(quit==False):
        solenoid_obj.release()
        print "Please wait for fan..."
        
        while(1):
            time.sleep(0.5)
            # Initalize sp and collect rpm(4 figures)
            pid_obj.setPoint(1500)
            rpm_value = int(rpm.get_rpm()) // 10
            print("rpm ", rpm_value)
            pv = int((pid_obj.update(rpm_value)))+ 64
            print ("pv ", pv)
            
            fan_obj.start_fan(pv)
            print("PWM: {0}\tRPM: {1}".format(pv,int(rpm.get_rpm())))
        
        
        print "Please load ball in on turret\n"
        solenoid_obj.block()
        time.sleep(5)
        solenoid_obj.release()
        print(rpm.get_rpm())
        print "And we have launch off!!!"
        
        
        
        print "Enter any number to stop fan: "
        
        user_key = input()
        fan_obj.stop_fan()
        print "Retry? Enter 1: "
        user_key = input()
        if(user_key==1):
            quit = False
        else:
            quit = True
            fan_obj.stop_fan()
    print "Program Terminated"
    GPIO.cleanup()


main() # run main

