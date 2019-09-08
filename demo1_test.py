
import RPi.GPIO as GPIO
# Setup for DC Fan
import wiringpi
import time

# Setup PWM for DC Fan
wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(18, 2)  # PWM output ONLY works on GPIO port 18

wiringpi.pwmSetClock(6)  # this parameters correspond to 25 KHz
wiringpi.pwmSetRange(128)

#*********************************************************************************************

def main():
    quit = False
    print "Welcome to Demo 1 of King Pong!\n"
    print "Loading -____-"
    DCfan(0)
    while(quit==False):
        GPIO.output(19, 0)
        print "Please wait for fan..."
        DCfan(100)
        print "Please load ball in on turret\n"
        GPIO.output(19, 1)
        time.sleep(5)
        GPIO.output(19, 0)
        print "And we have launch off!!!"
        print "Enter any number to stop fan: "
        user_key = input()
        DCfan(0)
        print "Retry? Enter 1: "
        user_key = input()
        if(user_key==1):
            quit = False
        else:
            quit = True
            DCfan(0)
    print "Program Terminated"
    GPIO.cleanup()


#---------------------------------------------------------------------------------------------
# Incorporate the fan into the main code running in parallel
# insert a delay waiting for the fan at full speeds

def DCfan(pwm):
    
    wiringpi.pwmWrite(18, pwm)  # maximum RPM
    time.sleep(5)

#---------------------------------------------------------------------------------------------

main() # run main
