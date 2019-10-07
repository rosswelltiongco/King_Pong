import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.

LimitSwitchUp = 22

GPIO.setup(LimitSwitchUp, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

class Limit_Switch:
    """""""""""""""""""""""""""""""""""""""
    " Execute function when switch is hit
    """""""""""""""""""""""""""""""""""""""
    def __init__(self, function):
        
        while(GPIO.input(LimitSwitchUp) == 0):
            # Wait until switch is hit
            pass
            
        function()
            
