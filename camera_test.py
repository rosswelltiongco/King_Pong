
# import the necessary packages
import numpy as np
import argparse
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
 
# load the image
image = cv2.imread(args["color.jpg"])

#convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#define color stregnth parameter in HSV
"""
#yellow color set
weaker = np.array([23, 100, 100])
stronger = np.array([40, 255, 255])

#green color set
weaker = np.array([70, 100, 100])
stronger = np.array([90, 255, 255])

#blue color set
weaker = np.array([110, 100, 100])
stronger = np.array([130, 255, 255])
"""
#upper RED color set
weaker = np.array([16, 100, 100])
stronger = np.array([179, 255, 255])

# lower/darker red color set
#weaker = np.array([0, 100, 100])
#stronger = np.array([10, 255, 255])


#threshold the HSV image to obtain input color
mask = cv2.inRange(hsv, weaker, stronger)
    