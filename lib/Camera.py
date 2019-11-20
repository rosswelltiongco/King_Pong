#importing modules
import cv2
import numpy as np
import os

import RPi.GPIO as GPIO
#from lib.Base import*
from Base import *
import time
import serial
#import Base

os.system("sudo modprobe bcm2835-v4l2")
cup_cascade = cv2.CascadeClassifier("/home/pi/Desktop/cups.xml")



#bc=0
class Camera:
    
    def __init__(self):
        self.base = Base()
        self.base.step_left(174)

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
        bc=0
        #print(self.cap.isOpened())
        while(1):
            _, img = self.cap.read()
            
            #converting frame(img i.e BGR) to HSV (hue-saturation-value)
            biggest =0
            hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            gray_scale = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            
            l_h = cv2.getTrackbarPos("L - H","Trackbars")
            l_s = cv2.getTrackbarPos("L - S","Trackbars")
            l_v = cv2.getTrackbarPos("L - V","Trackbars")
            u_h = cv2.getTrackbarPos("U - H","Trackbars")
            u_s = cv2.getTrackbarPos("U - S","Trackbars")
            u_v = cv2.getTrackbarPos("U - V","Trackbars")

            red_lower = np.array([170,200,10],np.uint8)
            red_upper = np.array([179,255,255],np.uint8)
            
            
            red_l = np.array([0,200,10],np.uint8)
            red_u = np.array([10,255,255],np.uint8)
            
            red = cv2.inRange(hsv, red_lower, red_upper)
            red2 = cv2.inRange(hsv,red_l,red_u)
            #Morphological transformation, Dilation     
            kernal = np.ones((5 ,5), "uint8")

            red=cv2.dilate(red, kernal) + cv2.dilate(red2,kernal)
            res=cv2.bitwise_and(img, img, mask = red)
            #Tracking the Red Color
            (_,contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            cup = cup_cascade.detectMultiScale(gray_scale)

            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                
                if(area >20000):
                    
                    x,y,w,h = cv2.boundingRect(contour)
                    for a,b,c,d in cup:
                        if a  <= x+w:
                            
                            print("red = " ,x  ," cup = " ,a -c )
                            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                            cv2.putText(img,"red party cup target",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
                            if w >= biggest & w < 640:
                                biggest = w
                                bc = x + w * .5
                        
            img = cv2.flip(img,flipCode = -1)
            cv2.imshow("Color Tracking",img)
            mask = cv2.inRange(hsv, red_lower, red_upper)  + cv2.inRange(hsv,red_l,red_u)
            res = cv2.bitwise_and(img,img, mask= mask)
            
            mask = cv2.flip(mask,flipCode = -1)
            res = cv2.flip(res,flipCode = -1)
            cv2.imshow('mask',mask)
            cv2.imshow('res',res)
            if(w == biggest):
                print("x = ", x, "y = ", y, "w = ", w, "h = ", h)
                bc =  x + .5 * w
                print("center = ", bc)
            
            
            if (bc > center+2):
                self.base.step_left(1)
                print("left")
            elif (bc < center-2):
                self.base.step_right(1)
                print("right")
            else:
                print("--------CENTERED-------")
                break
            

            if cv2.waitKey(10) & 0xFF == ord('q'):
                self.cap.release()
                cv2.destroyAllWindows()
                break
          
        return bc

camera = Camera()
camera.scan_cups()