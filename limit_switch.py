import RPi.GPIO as GPIO   # We need this library to access GPIO pins
from time import sleep

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
