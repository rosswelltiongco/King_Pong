import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
        # Port for Soleniod

class Solenoid:
    def __init__(self):
        """
        Initialize code
        """
        GPIO.output(19, 0)
    
    def block(self):
        GPIO.output(19, 1)
    
    def release(self):
        GPIO.output(19, 0)