import RPi.GPIO as GPIO   # We need this library to access GPIO pins
from time import sleep

<<<<<<< HEAD
GPIO.setmode(GPIO.BOARD)


LimitSwitchUp = 12 # The limit switch is connected to this pin


GPIO.setup(LimitSwitchUp, GPIO.IN)  # IN means we will listen to this pin

print "Turning motor on"



maxDur = 150
curDur = 0
pollInterval = 0.001
roomToGo = GPIO.input(LimitSwitchUp)

# We are now listening the status of the limit switch for
# 150 seconds, checking it every 0.001 seconds.
while roomToGo == 1 and curDur <= maxDur:
    sleep(pollInterval)
    curDur = curDur + pollInterval
    roomToGo = GPIO.input(LimitSwitchUp)

# Roll back down a little to release the switch
while GPIO.input(LimitSwitchUp) == 0:
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    
    
    sleep(pollInterval)

print "Stopping motor"

GPIO.cleanup()
=======
import time
import pigpio
import RPi.GPIO as GPIO

pi = pigpio.pi()
freq=5000
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22,GPIO.IN)
def int resetPos:
   
   if not pi.connected:
      exit()

   for pwm in range(500000, 1100000, 200000): # start from 50% and go up to 110% PWM
      pi.hardware_PWM(18, freq, pwm)
      print("\n12 set {} got {} pwm={}%".format(
      freq, pi.get_PWM_frequency(18),pwm/10000))
      time.sleep(5)

   pi.hardware_PWM(18, 0, 0)

   pi.stop()
   pos = 0
   return pos

GPIO.add_event_detect(22,GPIO.RISING,resetPos)
~
~
>>>>>>> 5cb819da8c93356f017b5f0933d6286b274d95ba
