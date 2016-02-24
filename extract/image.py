#!/usr/bin/env python2

import numpy as np
import scipy
import pymorph
from scipy import ndimage
import cv2
import matplotlib
import os
import sys
import time
import Utils
from Utils import printPylab, print_center
import re
from math import tan, atan, fabs
from decimal import Decimal

def get_target_data(img, lowbounds, highbounds):
  #convert to hsv
  #img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  #isolate colors to binary image
  #target_iso = cv2.inRange(img_hsv, lowbounds, highbounds)
  target_iso = cv2.inRange(img, lowbounds, highbounds)

  #Blur the binary image
  blur_target = ndimage.gaussian_filter(target_iso, 8)

  #Get contours of "true" pixel groups
  contours = get_contours(blur_target)
  largest_contour = get_largest_contour(contours)

  #Get x,y position and radius
#  target_info = get_target_info_from_contour(largest_contour)
  target_info = ((x,y), rad) = cv2.minEnclosingCircle(largest_contour)  

  cv2.circle(target_iso, (int(x), int(y)), int(rad), (100,100,100))
  cv2.imshow("image", target_iso)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  return target_info

def get_contours(binimg):
  contours, hierarchy = cv2.findContours(binimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  return contours

# def get_largest_contour_binimg(binimg):
#   """Given a binary image, detects the center of the largest contour"""
#   if contours:
#     cnt = getLargestContour(contours)
#     (x,y), radius = cv2.minEnclosingCircle(cnt)
#     center = (int(x),int(y))
#     return center
#   else:
#     return None

#def get_target_info_from_contour(contour):
#  (x,y), radius = cv2.minEnclosingCircle(contour)
#  return [[x,y], radius]

def get_largest_contour(contours):
  newlist = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
  return newlist[0]

RED_LOWER = np.array([17, 15, 100])
RED_UPPER = np.array([50, 56, 200])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "image.py imagefile"
        raise SystemExit
    img = cv2.imread(sys.argv[1])
    (x,y), radius = get_target_data(img, RED_LOWER, RED_UPPER)
    print (x,y), radius

