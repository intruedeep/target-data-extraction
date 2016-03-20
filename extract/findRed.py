#! /usr/bin/python

import numpy as np
from PIL import Image
import sys
import os
from image import image_contains_target, get_cv2_image_from_pil_image
import argparse
import time

# For PIL Method
R_THRESH = 140
G_THRESH = 80
B_THRESH = 80
PIXEL_THRESHOLD = 50

# For cv2 method
RED_LOWER = np.array([17, 15, 100])
RED_UPPER = np.array([50, 56, 200])
  


def custom_pixel_check(pil_img, pixel_thresh,red_thresh, green_thresh, blue_thresh):
  window = np.array(pil_img)
  imgHeight = window.shape[0]
  imgWidth = window.shape[1]
  pixel_count = 0
  for i in range(0, imgHeight):
    for j in range(0, imgWidth):
      if ( window[i][j][0] > red_thresh and window[i][j][1] < green_thresh and window[i][j][2] < blue_thresh ):
        pixel_count += 1

  return pixel_count > pixel_thresh


def setup_arg_parser(parser):
  """
  Given an argparse.ArgumentParser, sets it up to receive the 
  correct values for this script.
  """
  parser.add_argument("img_directory", help="the directory containing images to find the red in.")
  parser.add_argument("train_filename", help="a .txt file that will contain a key-value mapping between {image_name: presence_of_object}.")


def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  setup_arg_parser(parser)
  args = parser.parse_args()

  # Store arguments into variables
  img_directory = args.img_directory
  train_filename = args.train_filename


  trainList = open(train_filename, 'w')

  print("starting!!")


  oldtime = time.clock()
  files_in_dir = os.listdir(img_directory)
  for file_in_dir in files_in_dir:
    pil_img = Image.open(img_directory + file_in_dir)
    label = None


    if custom_pixel_check(pil_img, PIXEL_THRESHOLD, R_THRESH, G_THRESH, B_THRESH):
      cv2_img = get_cv2_image_from_pil_image(pil_img)
      if image_contains_target(cv2_img, RED_UPPER, RED_LOWER, PIXEL_THRESHOLD):
        label = '1'
      else:
        label = '0'
    else:
      label = '0'

    pil_img.close()

    # Write the train.txt file for convert_imageset.cpp
    trainList.write(img_directory + file_in_dir + ' ' + label + "\n")
    
    nowish = time.clock()
    delta = nowish - oldtime
    oldtime = nowish

    print("%d"%(delta));

  trainList.close() 

main()
