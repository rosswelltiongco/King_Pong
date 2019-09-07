# CECS 490 Project King Pong
# Demo1.py
# Created bv Mark Aquiapao
# Date: September 5, 2019
# Function: Shoot into (1) Cup

#*********************************************************************************************
# GPIO for Stepper Motor
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


# Setup for Stepper Motor
GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
control_pins = [7,11,13,15]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

halfstep_forward = [
   [1,0,0,0],
   [1,1,0,0],
   [0,1,0,0],
   [0,1,1,0],
   [0,0,1,0],
   [0,0,1,1],
   [0,0,0,1],
   [1,0,0,1]
]

halfstep_reverse = [
   [1,0,0,1],
   [0,0,0,1],
   [0,0,1,1],
   [0,0,1,0],
   [0,1,1,0],
   [0,1,0,0],
   [1,1,0,0],
   [1,0,0,0]
]


ROTATE_RIGHT = -1
ROTATE_LEFT = 1


# Constants for x and y
position_array = [0,1,2,3,4,5,6,7,8]
pwm_array = [0,1,2,3]  #associate with a pwm %

#pwm function, case statements, 0 - 50%, 1- 60%, 2-70%, 3-80%
pwm_value = 32

# 2d that depics base position and  pwm of fan
# two_d_array = [position_array, pwm_array]

current_x  = 4

# time sleep delays
delay_sensor = 10
delay_fan = 5
delay_shoot = 12

# Ports for Trig and Echo of ultrasonic sensor
TRIG = 16
ECHO = 18

# Port for Soleniod
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, 0)


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


#*********************************************************************************************

#send a done back to the while loop

#receive x and y
#run sensor to return a distance to trigger the system 50
#flag to determine if there's a cup present within the 50 - 70, then send a flag to trigger the system
#which x, new position using user input, to get the difference.
#which y, user input

#---------------------------------------------------------------------------------------------
# 2 dimensional array to control the time and the amount of steps to step for the motors
def stepperMotorBase(x, dir): # 0.03 = 30 ms
    
    print("Stepper Motor from Base is Turning!")
    
    if (dir == 1):
        for i in range(x): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep_forward[halfstep][pin])
                time.sleep(0.03)

    elif(dir == -1):
        for i in range(x): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep_reverse[halfstep][pin])
                    time.sleep(0.03)

    for pin in control_pins:
        GPIO.output(pin, 0)
        
    print("Finished Stepper Motor")

#---------------------------------------------------------------------------------------------
# Incorporate the fan into the main code running in parallel
# insert a delay waiting for the fan at full speeds

def DCfan(pwm):
    
    wiringpi.pwmWrite(18, pwm)  # maximum RPM
    time.sleep(5)

#---------------------------------------------------------------------------------------------
def distanceSensor():

    print"Distance Measurement In Progress"

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, False)

    print"Waiting For Sensor To Settle"

    #after 3 unit time then output
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

    print "Distance:" ,distance,"cm"
    
    if (20 < distance < 30):
        system_trigger = True
    else:
        system_trigger = False

    return system_trigger
#---------------------------------------------------------------------------------------------

main() # run main
