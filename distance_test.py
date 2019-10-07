# Import for all
import RPi.GPIO as GPIO
import fan
import solenoid
import time
import wiringpi

wiringpi.wiringPiSetupGpio()
wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

def main():
    fan_obj = fan.Fan()
    solenoid_obj = solenoid.Solenoid()
    
    calib = 45

    
    while 1:
        pwm_distances = [42, 45, 48, 51]
        selected_cup = int(input("Enter cup")) - 1
        pwm = pwm_distances[selected_cup]
        solenoid_obj.block()
        fan_obj.set_pwm(pwm)
        time.sleep(3)
        solenoid_obj.release()
        time.sleep(1) # Follow through
        fan_obj.set_pwm(0)
        
    GPIO.cleanup()




main() # run main