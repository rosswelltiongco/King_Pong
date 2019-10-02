# Import for all
import RPi.GPIO as GPIO
import fan
import solenoid
import time
import wiringpi
import rpm
import PID

wiringpi.wiringPiSetupGpio()
wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
        # Port for Soleniod
GPIO.setup(19, GPIO.OUT)

def main():
    fan_obj = fan.Fan()
    pid_obj = PID.PID()
    pwm = 64
    
    fan_obj.start_fan(pwm) # Roughly 15,000 RPM @ 9v
    
    while(1):
        pid_obj.setPoint(15000)
        ##print (rpm.get_rpm())
        #print("PWM: {0}\nRPM: {1}\nPV: {2}".format(pv,int(rpm.get_rpm()),pv))
        #time.sleep(1)
        # pv = pid_obj.update(rpm_val)
        #fan_obj.update_fan(55)
        
        # Initalize sp and collect rpm(4 figures)
        # print("rpm ", rpm_value)
        mv = int((pid_obj.update(int(rpm.get_rpm())))) + 64
        
        fan_obj.start_fan(mv)
        print("PWM: {0}\tRPM: {1}".format(mv,rpm.get_rpm()))
        
    GPIO.cleanup()


main()


