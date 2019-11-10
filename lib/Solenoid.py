import RPi.GPIO as GPIO

class Solenoid:
    # V+ - Diode
    
    def __init__(self,pin):
        """
        Initialize code
        """
        self.pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
        GPIO.setup(self.pin, GPIO.OUT)
        self.release()
    
    def block(self):
        GPIO.output(self.pin, 1)
    
    def release(self):
        GPIO.output(self.pin, 0)

