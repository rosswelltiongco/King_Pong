# Import for all
import RPi.GPIO as GPIO
import fan
import solenoid
import time
import wiringpi

wiringpi.wiringPiSetupGpio()
wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
        # Port for Soleniod
GPIO.setup(19, GPIO.OUT)

def main():
    fan_obj = fan.Fan()
    solenoid_obj = solenoid.Solenoid()
    quit = False
    print "Welcome to Demo 1 of King Pong!\n"
    print "Loading -____-"
    fan_obj.stop_fan()
    while(quit==False):
        solenoid_obj.release()
        print "Please wait for fan..."
        fan_obj.start_fan(41)
        print "Please load ball in on turret\n"
        solenoid_obj.block()
        time.sleep(5)
        solenoid_obj.release()
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
