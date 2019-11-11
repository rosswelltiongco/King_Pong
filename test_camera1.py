#importing modules

import cv2   
import numpy as np
import os


import RPi.GPIO as GPIO
from lib.Base import *
#from lib.Solenoid import*
#from lib.Display import*
import time
import serial

base = Base()

os.system("sudo modprobe bcm2835-v4l2")
TRIG = 40
ECHO = 38

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

scan_cup = {0: [5],
            1: [70],
            2: [145],
            3: [210],
            4: [300],
            5: [345],
            6: [405]}

def get_dist():
    try:
        #while True:

        GPIO.output(TRIG, False)
        #print "Waiting For Sensor To Settle"
        time.sleep(3)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
          pulse_start = time.time()

        while GPIO.input(ECHO)==1:
          pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)
        
        print ("Distance:",distance,"cm")
        return distance
    except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
        print("Cleaning up!")
        GPIO.cleanup()
          


def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H","Trackbars",0,179,nothing)
cv2.createTrackbar("L - S","Trackbars",0,255,nothing)
cv2.createTrackbar("L - V","Trackbars",0,255,nothing)
cv2.createTrackbar("U - H","Trackbars",179,179,nothing)
cv2.createTrackbar("U - S","Trackbars",255,255,nothing)
cv2.createTrackbar("U - V","Trackbars",255,255,nothing)


w = 0
x = 0
y = 0
h = 0
center = 310

base.step_left(100)

while(1):
    _, img = cap.read()
    
    #converting frame(img i.e BGR) to HSV (hue-saturation-value)
    img = cv2.flip(img,flipCode=-1)
    biggest =0
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    
    l_h = cv2.getTrackbarPos("L - H","Trackbars")
    l_s = cv2.getTrackbarPos("L - S","Trackbars")
    l_v = cv2.getTrackbarPos("L - V","Trackbars")
    u_h = cv2.getTrackbarPos("U - H","Trackbars")
    u_s = cv2.getTrackbarPos("U - S","Trackbars")
    u_v = cv2.getTrackbarPos("U - V","Trackbars")
    
    #red_lower = np.array([l_h,l_s,l_v],np.uint8)
    #red_upper = np.array([u_h,u_s,u_v],np.uint8)


    red_lower = np.array([152,36,0],np.uint8)
    red_upper = np.array([179,255,255],np.uint8)
    
    red=cv2.inRange(hsv, red_lower, red_upper)
    #Morphological transformation, Dilation     
    kernal = np.ones((5 ,5), "uint8")

    red=cv2.dilate(red, kernal)
    res=cv2.bitwise_and(img, img, mask = red)
    #Tracking the Red Color
    (_,contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        
        if(area>300):
            
            x,y,w,h = cv2.boundingRect(contour) 
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(img,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
            if w >= biggest & w < 640:
                biggest = w 
    cv2.imshow("Color Tracking",img)
    mask = cv2.inRange(hsv, red_lower, red_upper)
    res = cv2.bitwise_and(img,img, mask= mask)

    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    
    if(w == biggest):
        print("x = " , x , "y = ",y,"w=",w,"h=",h)
        bc =  x + .5 * w
        print("cup center = " ,bc)
    
    #base.step_right(10)
    
    if (bc > center+2):
        print("right")
        base.step_right(1)   
    elif (bc < center-2):
        print("left")
        base.step_left(1)
    else:
        print("centered")
        print(bc)
        print(base.get_pos())
        get_dist()
    

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
