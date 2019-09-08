# Import for all
import RPi.GPIO as GPIO
import fan
import solenoid
import time
#*********************************************************************************************

def main():
    fan_obj = fan.Fan()
    solenoid_obj = solenoid.Solenoid()
    fan_obj.start_fan(0)
    solenoid_obj.block()
    print "Please wait for fan..."
    fan_obj.start_fan(100)
    print "Please load ball in on turret\n"
    
    time.sleep(5)
    solenoid_obj.release()
    print "And we have launch off!!!"
    fan_obj.stop_fan()

    GPIO.cleanup()


main() # run main
