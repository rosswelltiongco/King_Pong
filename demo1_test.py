# Import for all
import RPi.GPIO as GPIO
import fan
import solenoid
import time
#*********************************************************************************************

def main():
    fan = fan.Fan()
    solenoid = solenoid.Solenoid()
    fan.start_fan(0)
    solenoid.block()
    print "Please wait for fan..."
    fan.start_fan(100)
    print "Please load ball in on turret\n"
    
    time.sleep(5)
    solenoid.release()
    print "And we have launch off!!!"
    fan.stop_fan()

    GPIO.cleanup()


main() # run main
