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

#_-__-_________--___--_--_ultra sonic sensor code _______-_----__--___-__-

TRIG = 16
ECHO = 18

print"Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

print"Waiting For Sensor To Settle"

#after 5 unit time then output
time.sleep(5)
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




def main():
    
    print "Welcome to King Pong!"
    #stepperMotorBase(16, 1)  # 90 degrees
    while (40 < distance < 50):
        DCfan(input()) # max RPM
    #stepperMotorBase(16, -1) # 90 degrees other way
    
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
