#!/usr/bin/env python

import time
import pigpio

pi = pigpio.pi()
freq=5000

if not pi.connected:
   exit()

for pwm in range(500000, 1100000, 200000): # start from 50% and go up to 110% PWM
   pi.hardware_PWM(18, freq, pwm)
   print("\n12 set {} got {} pwm={}%".format(
     freq, pi.get_PWM_frequency(18),pwm/10000))
   time.sleep(5)

pi.hardware_PWM(18, 0, 0)

pi.stop()
~
~
