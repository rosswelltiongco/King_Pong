import RPi.GPIO as GPIO
import wiringpi
import time

class Fan:
    def __init__(self):
        """
        Initialize code
        
        setClock = 6
        setRange = 128
        19.2e6 fan 
        #How the math works
        
        #25 kHz = (19.2 * 10^6) / 6 / 128
        # Setup PWM for DC Fan
        """
        wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

        wiringpi.wiringPiSetupGpio()

        wiringpi.pinMode(18, 2)  # PWM output ONLY works on GPIO port 18

        wiringpi.pwmSetClock(6)  # this parameters correspond to 25 KHz #192
        wiringpi.pwmSetRange(128) # 4096

        self.set_pwm(0)

    def set_pwm(self,pwm):
        wiringpi.pwmWrite(18,pwm)
