# CECS 490 Project King Pong

# Syntax for Main loop

# Make 2D for set of cups(10x4)

# While(done != true)

#  Run Sensor and Camera Functions
#  Returns Index Value for which Cup(X) and PWM Value(Y)
#  PWM is entered by user input
#  Run Stepper Motor Code to Move Base to Index(X value)
#  Run DC Fan Code that will start the fan with Y value
#  Use timer to have a delay
#  Run Loading Code to load ball into pipe with fan on at desired
#  PWM
#  Use timer for delay in making sure ball is in cup and cup is taken out
#  Set index = 4(intial)
#  Run Stepper Motor Function to reset index
#  Set done = TRUE

# End of While Loop

# Set done = FALSE outside of while loop in main()
# To continue loop

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
control_pins_left  = [7,11,13,15]
control_pins_right = [3,5,8,10]

for pin in control_pins_left:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

for pin in control_pins_right:
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



ROTATE_RIGHT = 1
ROTATE_LEFT = -1


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
GPIO.output(pin, 0)


#*********************************************************************************************

def main():
    new_x=1; difference=0; DCfan(0);
    print "Welcome to Demo 2 of King Pong!"
    print " "
    stepperMotorBase(16, -1)
    for current_x in range(1, 5, 1):
        if(current_x==1):
            difference = new_x-current_x
            steps = difference * 32
            print "Initial Steps"
            print "Current position: ", current_x
            print "New Position    : ", new_x
            print "Difference      : ", difference
            print "Steps           : ", steps
    
        if(current_x<=4):
            #stepperMotorBase(steps, -1)
            DCfan(128)
            #GPIO.output(pin, 1)
            print "Finished Cup(", current_x, ")"
            #GPIO.output(pin, 0)
            DCfan(0) # Fan is Off
            new_x = current_x+1
            difference = new_x-current_x
            steps = difference * 32
            print "Updated Steps"
            print "Current position: ", current_x
            print "New Position    : ", new_x
            print "Difference      : ", difference
            print "Steps           : ", steps
            print " "
            print " "
        else:
            break
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
                    GPIO.output(control_pins_left[pin], halfstep_forward[halfstep][pin])
                    GPIO.output(control_pins_right[pin], halfstep_forward[halfstep][pin])
                time.sleep(0.03)

    elif(dir == -1): # turning left
        for i in range(x): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_right[pin], halfstep_reverse[halfstep][pin])
                    GPIO.output(control_pins_left[pin], halfstep_reverse[halfstep][pin])
                time.sleep(0.03)

for pin in control_pins_left:
    GPIO.output(pin, 0)
    
    for pin in control_pins_right:
        GPIO.output(pin, 0)

print("Finished Stepper Motors")

#---------------------------------------------------------------------------------------------
# Incorporate the fan into the main code running in parallel
# insert a delay waiting for the fan at full speeds

def DCfan(pwm):
    
    print "PWM: ", pwm
    wiringpi.pwmWrite(18, pwm)  # maximum RPM
    time.sleep(1)
    print("Fan Done")

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
