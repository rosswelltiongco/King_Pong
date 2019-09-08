
import wiringpi
import time
wiringpi.pwmSetMode(0) # PWM_MODE_MS = 0

wiringpi.wiringPiSetupGpio()  

wiringpi.pinMode(18, 2)      # pwm only works on GPIO port 18  

wiringpi.pwmSetClock(6)  # this parameters correspond to 25kHz --at what clock freq will it run the best
# only port 18 will work with pwm 

wiringpi.pwmSetRange(128)

print("Press any key to start")
input()
time.sleep(2)
wiringpi.pwmWrite(18, 0)   # minimum RPM
print("PWM: 0")
#there needs to be an assertion of delay for the fan to be ready operating at full speed

time.sleep(5)
wiringpi.pwmWrite(18, 128)  # maximum RPM

time.sleep(3)

print("PWM: 128")     
#time.sleep(3)
#print("PWM: 0") 
wiringpi.pwmWrite(18, 0)  # maximum RPM
time.sleep(3)


time.sleep(3)

wiringpi.pwmWrite(18, 128)  # maximum RPM
print("PWM: 128")     
time.sleep(5)
print("PWM: 0")

wiringpi.pwmWrite(18, 0)  # maximum RPM
time.sleep(3)
print("fisnihed") 
