import RPi.GPIO as GPIO
import time     
GPIO.setwarnings(False)



GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
# Pins [1,3,4,2] -> 1 = Outer Left, 4 = Outer right, Heat Sink facing down on H-Bridge
control_pins_left = [15,11,7,13]
control_pins_right = [10,5,16,8]

LimitSwitchUp = 22

GPIO.setup(LimitSwitchUp, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#global rightBoundry,leftBoundry, pos

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
    def __init__(self, pos):    
    
        self.pos = pos
        self.boundary_left = 400
        self.boundary_right = 0


        for pin in control_pins_left:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, 0)
            
        for pin in control_pins_right:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        
        GPIO.setup(22,GPIO.IN)
        while(GPIO.input(LimitSwitchUp)==0): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_left[pin], halfstep_forward[halfstep][pin])
                    GPIO.output(control_pins_right[pin], halfstep_forward[halfstep][pin])
                time.sleep(0.01)

        #print(leftBoundry)


    def move_right(self, delta):
        """
        print("Moving right {}".format(delta))
        for step in range(delta):
            if self.pos <= self.boundary_right:
                break # pass or break
            else:
                self.pos -= 1
            print(self.pos)

    
        Args:
            - steps (int): value to move stepper motor in desired position
        
        Runs based on x in the right direction
        """
        
        if(delta > self.boundary_right):
            delta = self.pos 
        elif (delta < self.boundary_right):
            delta = delta
            
            
        print(self.pos)
        print("Base is Turning!")
        
        for i in range(delta): # 90 degrees
            print(self.pos)
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_left[pin], halfstep_forward[halfstep][pin])
                    GPIO.output(control_pins_right[pin], halfstep_forward[halfstep][pin])
                time.sleep(0.01)
            self.pos -= 1
        for pin in control_pins_left:
            GPIO.output(pin, 0)
            
        for pin in control_pins_right:
            GPIO.output(pin, 0)


        
    def move_left(self, delta):

        """
        Args:
            - steps (int): value to move stepper motor in desired position
        
        Runs based on x in the right direction
       
        
        
        print("Moving left {}".format(delta))
        
        
        for step in range(delta):
            
            if self.pos >= self.boundary_left:
                break # pass or break
            else:
                self.pos += 1
            print(self.pos)
        #print("Base is Turning!")
            
        
        """
        if(self.pos + delta  > self.boundary_left):
            delta = (self.pos + delta)  - (delta - self.boundary_left) 
        #elif (self.pos + delta):
         #   delta = delta - self.pos
        
        for i in range(delta): # 90 degrees
            print(self.pos)
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_left[pin], halfstep_reverse[halfstep][pin])
                    GPIO.output(control_pins_right[pin], halfstep_reverse[halfstep][pin])
                time.sleep(0.01)
            self.pos += 1
            
        for pin in control_pins_left:
            GPIO.output(pin, 0)
            
        for pin in control_pins_right:
            GPIO.output(pin, 0) 

        

#base = Base(0)
#base.move_left(75)
#base.move_right(50)

"""
base.move_right(150)
base.move_left(200)
base.move_right(200)
"""
