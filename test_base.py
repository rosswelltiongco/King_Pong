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
control_pins_left = [15,11,7,13]
control_pins_right = [10,5,3,8]


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

#_-__-_________--___--_--_ultra sonic sensor code _______-_----__--___-__-
#Specify by pin number not by GPIO number

# Constants for x and y 
position_array = [0,1,2,3,4,5,6,7,8]
pwm_array = [0,1,2,3]  #associate with a pwm %

#pwm function, case statements, 0 - 50%, 1- 60%, 2-70%, 3-80%


INITIAL = 4
current_x  = 4
previous_x = 4
new_x = 0
difference_x = new_x - current_x

delay_sensor = 10
delay_fan = 5
delay_shoot = 12





def main():
    
    print "Welcome to King Pong!"
    
    stepperMotorBase(64, 1)
    
    stepperMotorBase(64, -1)
    GPIO.cleanup()

# 2 dimensional array to control the time and the amount of steps to step for the motors
def stepperMotorBase(x, dir): # 0.03 = 30 ms
    
    print("Stepper Motor from Base is Turning!")
    
    if (dir ==1):
        for i in range(x): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_left[pin], halfstep_forward[halfstep][pin])
                    GPIO.output(control_pins_right[pin], halfstep_forward[halfstep][pin])
                time.sleep(0.03)

    if(dir ==-1):
        for i in range(x): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_left[pin], halfstep_reverse[halfstep][pin])
                    GPIO.output(control_pins_right[pin], halfstep_reverse[halfstep][pin])
                time.sleep(0.03)

    for pin in control_pins_left:
        GPIO.output(pin, 0)
        
    for pin in control_pins_right:
        GPIO.output(pin, 0)
        
    print("Finished Stepper Motor")
    
    
# Incorporate the fan into the main code running in parallel
# insert a delay waiting for the fan at full speeds

def DCfan(pwm):
    
    
    print("Fan is turning on in 3 seconds")
    print"3"
    time.sleep(1)
    print"2"
    time.sleep(1)
    print"1"
    time.sleep(1)
    
    wiringpi.pwmWrite(18, 0)   # minimum RPM
    print("PWM: 0")
    #there needs to be an assertion of delay for the fan to be ready operating at full speed


    #100% test
    print("PWM: 128 100% for 5") 
    wiringpi.pwmWrite(18, 90)  # maximum RPM
    time.sleep(10)
    
    print("sleep for 20")
    wiringpi.pwmWrite(18, 0)  # maximum RPM
    time.sleep(10)
    
    
   #90% test 
    print("PWM: 115 90% for 5") 
    wiringpi.pwmWrite(18, 90)  # maximum RPM
    time.sleep(10)
    
    
    print("sleep for 20")
    wiringpi.pwmWrite(18, 0)  # maximum RPM
    time.sleep(10)
    print("Finished Fan")
    
   #90% test 
    print("PWM: 100 80% for 5") 
    wiringpi.pwmWrite(18, 90)  # maximum RPM
    time.sleep(10)
    
    
    print("sleep for 20")
    wiringpi.pwmWrite(18, 0)  # maximum RPM
    time.sleep(10)


   #70% test 
    print("PWM: 90 70% for 5") 
    wiringpi.pwmWrite(18, 90)  # maximum RPM
    time.sleep(10)
    
    
    print("sleep for 20")
    wiringpi.pwmWrite(18, 0)  # maximum RPM
    time.sleep(10)
    
    #60% test 
    print("PWM: 77 60% for 10") 
    wiringpi.pwmWrite(18, 90)  # maximum RPM
    time.sleep(10)
    
    
    print("sleep for 5")
    wiringpi.pwmWrite(18, 0)  # maximum RPM
    time.sleep(5)
    print("Finished Fan")
    
    
    wiringpi.pwmWrite(18, 0)  # maximum RPM
main()

