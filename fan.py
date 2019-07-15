
import wiringpi
import time
wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

wiringpi.wiringPiSetupGpio()  

wiringpi.pinMode(18, 2)      # pwm only works on GPIO port 18  

wiringpi.pwmSetClock(6)  # this parameters correspond to 25kHz
wiringpi.pwmSetRange(128)

print("Press any key to start")
input()
time.sleep(2)
wiringpi.pwmWrite(18, 0)   # minimum RPM
print("PWM: 0")
time.sleep(2)
wiringpi.pwmWrite(18, 128)  # maximum RPM
print("PWM: 128")
time.sleep(3)
print("PWM: 0")
wiringpi.pwmWrite(18, 0)

print("Finished")


