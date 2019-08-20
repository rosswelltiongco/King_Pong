# CECS 490 Project King Pong

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
GPIO.setmode(GPIO.BOARD)
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

def main():
    
    print "Welcome to King Pong!"
    stepperMotorBase(16, 1)  # 90 degrees
    DCfan(128) # max RPM
    stepperMotorBase(16, -1) # 90 degrees other way
    
    GPIO.cleanup()

# 2 dimensional array to control the time and the amount of steps to step for the motors
def stepperMotorBase(x, dir): # 0.03 = 30 ms
    
    print("Stepper Motor from Base is Turning!")
    
    if (dir ==1):
        for i in range(x): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep_forward[halfstep][pin])
                time.sleep(0.03)

    if(dir ==-1):
        for i in range(x): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep_reverse[halfstep][pin])
                time.sleep(0.03)

    for pin in control_pins:
        GPIO.output(pin, 0)
        
    print("Finished Stepper Motor")
    
    
# Incorporate the fan into the main code running in parallel
# insert a delay waiting for the fan at full speeds

def DCfan(pwm):
    
    print("Press any key to start")
    input()
    time.sleep(2)
    wiringpi.pwmWrite(18, 0)   # minimum RPM
    print("PWM: 0")
    #there needs to be an assertion of delay for the fan to be ready operating at full speed

    time.sleep(5)
    wiringpi.pwmWrite(18, 128)  # maximum RPM

    time.sleep(3)

    print("PWM: 128")     
    #time.sleep(3)
    #print("PWM: 0") 
    wiringpi.pwmWrite(18, 0)  # maximum RPM
    time.sleep(3)

    wiringpi.pwmWrite(18, 128)  # maximum RPM
    print("PWM: 128")     
    time.sleep(5)
    print("PWM: 0")

    wiringpi.pwmWrite(18, 0)  # maximum RPM
    time.sleep(3)
    print("Finished Fan")  

main()