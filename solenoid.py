import RPi.GPIO as GPIO



class Solenoid:
    def __init__(self):
        """
        Initialize code
        """
        GPIO.output(19, 0)
    
    def block():
        GPIO.output(19, 0)
    
    def release():
        GPIO.output(19, 1)