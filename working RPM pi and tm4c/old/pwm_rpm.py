# Import for all
import RPi.GPIO as GPIO
import time
#import wiringpi
import rpm

wiringpi.wiringPiSetupGpio()
wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #this cmd is for user to specify pin as number of the board.
        # Port for Soleniod
GPIO.setup(19, GPIO.OUT)


def graph(pwm_values,rpm_values):
    import matplotlib.pyplot as plt
    
    print(pwm_values)
    print(rpm_values)
    
    plt.plot(pwm_values, rpm_values)
    plt.xlabel('PWM')
    plt.ylabel('RPM')
    plt.xlim([20,60])
    plt.ylim([50,250])
    plt.show()
    
    pass


def main():
    rpm_val = int(rpm.get_rpm()) // 10
    #time.sleep(1)
    """
    fan_obj = fan.Fan()
    solenoid_obj = solenoid.Solenoid()
    fan_obj.start_fan(0)
    time.sleep(2)
    
    pwm_values = []
    rpm_values = []
    for count in range(29, 61, 15):
        fan_obj.start_fan(count)
        pwm_values.append(count)
        rpm_val = int(rpm.get_rpm()) // 10
        #rpm_values.append(rpm_val)
        print("PWM: {0}\tRPM: {1}".format(count,rpm_val))
    
    #GPIO.cleanup()
    #solenoid_obj.release()
    #graph(pwm_values,rpm_values)
    print("Enter a desired RPM.")
    
    trpm = int(input("Enter a desired RPM."))
    while(1):
        print("works")
        rpm_val = int(rpm.get_rpm()) // 10
        if(trpm > rpm_val):
            count = count + 1
        if(trpm< rpm_val):
            count = count - 1
        else:
            #solenoid_obj.release()
            print("PWM: {0}\tRPM: {1}".format(count,rpm_val))
            print("______EQUAL________")
            #time.sleep(1)
            count = count
            solenoid_obj.block()
            time.sleep(1)
            
            solenoid_obj.release()
            
        fan_obj.start_fan(count)
        print("PWM: {0}\tRPM: {1}".format(count,rpm_val))
    """
    GPIO.cleanup()
main() # run main


