# Import for all
import RPi.GPIO as GPIO
import fan
import solenoid
import time
import wiringpi

wiringpi.wiringPiSetupGpio()
wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
        # Port for Soleniod
GPIO.setup(19, GPIO.OUT)

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
