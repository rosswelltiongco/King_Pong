import RPi.GPIO as GPIO
import time
import serial

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)




class Sensor:
    def __init__(self):
        
        self.TRIG = 40
        self.ECHO = 38
        
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.output(self.TRIG, False)
        
        GPIO.setup(self.ECHO, GPIO.IN)
            

            
    def get_distance(self):
        try:
            
            #print "Waiting For Sensor To Settle"
            time.sleep(3)
            
            GPIO.output(self.TRIG, True)
            time.sleep(0.00001)
            GPIO.output(self.TRIG, False)
        
            while GPIO.input(self.ECHO)==0:
                pass
                pulse_start = time.time()

            while GPIO.input(self.ECHO)==1:
                pass
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration * 17150

            distance = round(distance, 2)
            
            print(distance)
            return distance
        
        except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
            print("Cleaning up!")
            GPIO.cleanup()

sensor = Sensor()
sensor.get_distance()