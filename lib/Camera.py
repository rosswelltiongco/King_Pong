#importing modules
import cv2
import numpy as np
import os

import RPi.GPIO as GPIO
from lib.Base import*
import time
import serial

os.system("sudo modprobe bcm2835-v4l2")


base = Base()
class Camera:
    
    def __init__(self):
        base.step_left(100)

        self.cap = cv2.VideoCapture(0)
        
        
        """
        cv2.namedWindow("Trackbars")
        cv2.createTrackbar("L - H","Trackbars",0,179,nothing)
        cv2.createTrackbar("L - S","Trackbars",0,255,nothing)
        cv2.createTrackbar("L - V","Trackbars",0,255,nothing)
        cv2.createTrackbar("U - H","Trackbars",179,179,nothing)
        cv2.createTrackbar("U - S","Trackbars",255,255,nothing)
        cv2.createTrackbar("U - V","Trackbars",255,255,nothing)
        """
        
    
    
    def scan_cups(self):
    
        w = 0
        x = 0
        y = 0
        h = 0
        center = 310

        while(1):
            _, img = self.cap.read()
            
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
                bc =  x + .5 * w
            
            
            if (bc > center+2):
                base.step_right(1)   
            elif (bc < center-2):
                base.step_left(1)
            else:
                break
            

            if cv2.waitKey(10) & 0xFF == ord('q'):
                self.cap.release()
                cv2.destroyAllWindows()
                break
          
        return bc