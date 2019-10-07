import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
# Pins [1,3,4,2] -> 1 = Outer Left, 4 = Outer right, Heat Sink facing down on H-Bridge
control_pins_left = [15,11,7,13]
control_pins_right = [10,5,16,8]

LimitSwitchUp = 22

GPIO.setup(LimitSwitchUp, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

global rightBoundry,leftBoundry, pos

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

class Base:
    
    def __init__(self):
        global pos
        global leftBoundry
        global rightBoundry
        for pin in control_pins_left:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
            
        for pin in control_pins_right:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        
        GPIO.setup(22,GPIO.IN)
        leftBoundry = 0
        while(GPIO.input(LimitSwitchUp)==0): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_left[pin], halfstep_forward[halfstep][pin])
                    GPIO.output(control_pins_right[pin], halfstep_forward[halfstep][pin])
                time.sleep(0.01)
                
                leftBoundry = leftBoundry + 1
        rightBoundry = 0
        leftBoundry = 100
        pos = 0
        print(leftBoundry)
      
        
        
    def move_right(self, steps): 
        
        """
        Args:
            - steps (int): value to move stepper motor in desired position
        
        Runs based on x in the right direction
        """
        
        print("Base is Turning!")
        
        for i in range(steps): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_left[pin], halfstep_forward[halfstep][pin])
                    GPIO.output(control_pins_right[pin], halfstep_forward[halfstep][pin])
                time.sleep(0.0001)

        for pin in control_pins_left:
            GPIO.output(pin, 0)
            
        for pin in control_pins_right:
            GPIO.output(pin, 0)
            
            
    def move_left(self, steps):
        global pos
        global leftBoundry
        global rightBoundry
        """
        Args:
            - steps   (int): value to move stepper motor in desired position
        
        Runs based on x in left direction
        """
        currPos = 0
        while (GPIO.input(LimitSwitchUp)==0) or (pos > 100):
            for i in range(steps): # 90 degrees
                for halfstep in range(8):
                    for pin in range(4):
                        GPIO.output(control_pins_left[pin], halfstep_reverse[halfstep][pin])
                        GPIO.output(control_pins_right[pin], halfstep_reverse[halfstep][pin])
                    time.sleep(0.004)
                pos = pos + 1
                currPos = pos
                print(pos)

        for pin in control_pins_left:
            GPIO.output(pin, 0)
            
        for pin in control_pins_right:
            GPIO.output(pin, 0)

    
    
    def stop_base(self, steps):
        
        for i in range(steps): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_left[pin], halfstep_reverse[halfstep][pin])
                    GPIO.output(control_pins_right[pin], halfstep_reverse[halfstep][pin])
                time.sleep(0.01)

        for pin in control_pins_left:
            GPIO.output(pin, 0)
            
        for pin in control_pins_right:
            GPIO.output(pin, 0)