#!/usr/bin/env python2

import numpy as np
from scipy import ndimage
import cv2
import sys

def get_target_data(img, lowbounds, highbounds):
  #isolate colors to binary image
  target_iso = cv2.inRange(img, lowbounds, highbounds)

  #Blur the binary image
  blur_target = ndimage.gaussian_filter(target_iso, 8)

  # Get contours and keep the largest - this should be our target
  contours, _ = cv2.findContours(blur_target, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  largest_contour = max(contours, key=lambda x: cv2.contourArea(x))

  #Get x,y position and radius
  (x,y), rad = cv2.minEnclosingCircle(largest_contour)  

  xi = int(x)
  yi = int(y)
  tl = (xi-5,yi-5)
  tr = (xi+5,yi-5)
  bl = (xi-5,yi+5)
  br = (xi+5,yi+5)

  # draw two intersecting lines each 10 pixels long and a bounding circle
  cv2.line(img, tl, br, (50, 200, 50), thickness=2)
  cv2.line(img, tr, bl, (50, 200, 50), thickness=2)
  cv2.circle(img, (xi, yi), int(rad), (100,100,100))

  # cv2.imshow("image", img)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()

  return ((x,y), rad)

RED_LOWER = np.array([17, 15, 100])
RED_UPPER = np.array([50, 56, 200])


def area_containing_target(img, highbounds, lowbounds):
  #isolate colors to binary image
  target_iso = cv2.inRange(img, lowbounds, highbounds)

  #Blur the binary image
  blur_target = ndimage.gaussian_filter(target_iso, 8)

  # Get contours and keep the largest - this should be our target
  contours, _ = cv2.findContours(blur_target, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  largest_contour = max(contours, key=lambda x: cv2.contourArea(x))

  area = cv2.contourArea(largest_contour)
  return area

def image_contains_target(img, highbounds, lowbounds, count_threshold):
  area = area_containing_target(img, highbounds, lowbounds)

  return area >= count_threshold


def get_cv2_image_from_pil_image(pil_img):
  open_cv_image = np.array(pil_img) 
  # Convert RGB to BGR 
  open_cv_image = open_cv_image[:, :, ::-1].copy()
  return open_cv_image


if __name__ == '__main__':
    """ This script needs some testing. Also a helpful 'view-next' feature should
        be implemented to quickly verify cv2 results. 
    """
    if len(sys.argv) < 2:
        print "image.py imagefile"
        raise SystemExit
    img = cv2.imread(sys.argv[1])
    (x,y), radius = get_target_data(img, RED_LOWER, RED_UPPER)
    print (x,y), radius

