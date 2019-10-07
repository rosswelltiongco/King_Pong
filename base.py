# CECS 490 Project King Pong

# Class file for the stepper motor controlling the base

# GPIO for Stepper Motor
import RPi.GPIO as GPIO
import time


# Setup for Stepper Motor
GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
# Pins [1,3,4,2] -> 1 = Outer Left, 4 = Outer right, Heat Sink facing down on H-Bridge
control_pins_left = [15,11,7,13]
<<<<<<< HEAD
control_pins_right = [10,5,16,8]

=======
control_pins_right = [10,5,3,8]
int pos
>>>>>>> 5cb819da8c93356f017b5f0933d6286b274d95ba
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
        """
        Initialize code
        """

        for pin in control_pins_left:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
            
        for pin in control_pins_right:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        GPIO.setup(22,GPIO.IN)

        while(!GPIO.input(22)): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_left[pin], halfstep_forward[halfstep][pin])
                    GPIO.output(control_pins_right[pin], halfstep_forward[halfstep][pin])
                time.sleep(0.01)

        pos = 0
      
        
        
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
                time.sleep(0.01)

        for pin in control_pins_left:
            GPIO.output(pin, 0)
            
        for pin in control_pins_right:
            GPIO.output(pin, 0)
            
            
    def move_left(self, steps):
        
        """
        Args:
            - steps   (int): value to move stepper motor in desired position
        
        Runs based on x in left direction
        """
    
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
<<<<<<< HEAD
    
    
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
            
    
=======

    def reset():
      pos = 0


GPIO.add_event_detect(22,GPIO.RISING,reset)
>>>>>>> 5cb819da8c93356f017b5f0933d6286b274d95ba
