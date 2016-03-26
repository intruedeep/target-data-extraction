#! /usr/bin/python

import numpy as np
from PIL import Image
import sys
import os
from image import image_contains_target, get_cv2_image_from_pil_image
import argparse
import time

# For PIL Method
R_THRESH = 100
G_THRESH = 80
B_THRESH = 80
PIXEL_THRESHOLD = 29

# For cv2 method
RED_LOWER = np.array([0, 0, 100])
RED_UPPER = np.array([80, 80, 200])  

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

  oldtime = time.clock()
  files_in_dir = os.listdir(img_directory)
  for file_in_dir in files_in_dir:
    pil_img = Image.open(img_directory + file_in_dir)
    label = None
    skVote = '0'
    lukeVote = '0'

    cv2_img = get_cv2_image_from_pil_image(pil_img)

    start = time.clock()
    check = image_contains_target(cv2_img, RED_UPPER, RED_LOWER, PIXEL_THRESHOLD)
    end = time.clock()

    delta = end - start
    
    print("time cv %.03f"%(delta));
    
    start = time.clock()
    checkCustom = custom_pixel_check(pil_img, PIXEL_THRESHOLD, R_THRESH, G_THRESH, B_THRESH)
    end = time.clock()

    delta = end - start

    print("time custom %.03f"%(delta));

    if checkCustom:
      skVote = '1'
    else:
      skVote = '0'

    if check == -2:
      lukeVote = '0'
    elif check:
      lukeVote = '1'
    else:
      lukeVote = '0'

    if skVote != lukeVote:
      disagree = True
    else:
      disagree = False

    if lukeVote == '1':
      label = '1'
    else:
      label = '0'

    pil_img.close()

    # Write the train.txt file for convert_imageset.cpp
    trainList.write(img_directory + file_in_dir + ' ' + label + "\n")
    print lukeVote, skVote
    if disagree:
      print "disagreement: ", img_directory + file_in_dir + " " + lukeVote + " " + skVote
    nowish = time.clock()
    delta = nowish - oldtime
    oldtime = nowish

    #print("%.03f"%(delta));

  trainList.close() 

main()
