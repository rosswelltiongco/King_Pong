import RPi.GPIO as GPIO
from lib.Base import *
import time

base = Base()


def main():
    while 1:
        base.go_to(int(input("Enter position")))
        #base.step_right(200)
    GPIO.cleanup()
main()