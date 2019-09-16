# Import for all
import RPi.GPIO as GPIO
import fan
import solenoid
import time
import wiringpi
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
    
    plt.plot(pwm_values, rpm_values, 'ro')
    plt.xlabel('PWM')
    plt.ylabel('RPM')
    plt.xlim([0,128])
    plt.ylim([0,250])
    plt.show()

def main():
    fan_obj = fan.Fan()
    
    pwm_values = []
    rpm_values = []
    
    for count in range(0,127, 16):
        fan_obj.start_fan(count)
        pwm_values.append(count)
        rpm_val = int(rpm.get_rpm()) // 100
        rpm_values.append(rpm_val)
        print("PWM: {0}\tRPM: {1}".format(count,rpm_val))
    
    GPIO.cleanup()

    
    graph(pwm_values,rpm_values)

main() # run main


