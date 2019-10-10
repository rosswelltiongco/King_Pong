import RPi.GPIO as GPIO
import time

class Solenoid:
    # V+ - Diode
    
    def __init__(self):
        """
        Initialize code
        """
        self.pin = 19
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
        GPIO.setup(self.pin, GPIO.OUT)
        self.release()
    
    def block(self):
        GPIO.output(self.pin, 1)
    
    def release(self):
        GPIO.output(self.pin, 0)

solenoid = Solenoid() 
solenoid.block()
time.sleep(2)
solenoid.release()