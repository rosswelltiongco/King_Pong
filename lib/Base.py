# FIXME: Breakout bug when target exceeds left boundary
# Followup note: if we use targeet placement system, do we need boundary checks? Keep boundary checks for now

import RPi.GPIO as GPIO
import time     
GPIO.setwarnings(False)


GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
# Pins [1,3,4,2] -> 1 = Outer Left, 4 = Outer right, Heat Sink facing down on H-Bridge
control_pins_left = [15,11,7,13]

LimitSwitchUp = 22

GPIO.setup(LimitSwitchUp, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

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
    
        self.pos = 0
        self.BOUND_LEFT = 394
        self.BOUND_RIGHT = 0
        self.SPEED = 0.002
        
        GPIO.setup(22,GPIO.IN)
        
        self.on()
        
        while(GPIO.input(LimitSwitchUp)==0): # 90 degrees
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins_left[pin], halfstep_forward[halfstep][pin])
                time.sleep(self.SPEED)
        
        self.off()
        
    def step_right(self, steps):
        """
        if(delta > self.boundary_right):
            delta = self.pos 
        elif (delta < self.boundary_right):
            delta = delta
        """
        
        self.on()
        
        
        for i in range(steps):
            if self.pos <= self.BOUND_RIGHT:
                break
            else:
                for halfstep in range(8):
                    for pin in range(4):
                        GPIO.output(control_pins_left[pin], halfstep_forward[halfstep][pin])
                    time.sleep(self.SPEED)
                self.pos -= 1
        self.off()


        
    def step_left(self, steps):
        """
        if(self.pos + delta  > self.boundary_left):
            delta = (self.pos + delta)  - (delta - self.boundary_left) 
           
        """
        
        self.on()
        
            
        for i in range(steps):
            if self.pos >= self.BOUND_LEFT:
                break
            else:
                for halfstep in range(8):
                    for pin in range(4):
                        GPIO.output(control_pins_left[pin], halfstep_reverse[halfstep][pin])
                    time.sleep(self.SPEED)
                self.pos += 1
        self.off()
    def get_pos(self):
        return self.pos
    def on(self):
        for pin in control_pins_left:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, 0)
    
    def off(self):
        for pin in control_pins_left:
            GPIO.output(pin, 0)

    def go_to(self,target):
        if self.pos < target:
            while self.pos < target:
                self.step_left(1)
        else:
            while self.pos > target:
                self.step_right(1)

