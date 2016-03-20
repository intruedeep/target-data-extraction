import cv2
import argparse
import os, sys
from image import get_target_data as get_image_target_data
import numpy as np
# import UI



def setup_arg_parser(parser):
  """
  Given an argparse.ArgumentParser, sets it up to receive the 
  correct values for this script.
  """
  parser.add_argument("input_mp4", help="the mp4 file to generate frames from.")
  parser.add_argument("output_folder", help="the folder to store the frames.")

def get_target_data_from_video(vidcap, lowbounds, highbounds):
  count = 0;
  success = True
  retlist = []
  while success:
    success,image = vidcap.read()

    #metadata = get_image_target_data(image, np.array([80,80,100]), np.array([255,255,255]))
    metadata = []

    retlist.append([image, metadata])
    if cv2.waitKey(10) == 27:                     # exit if Escape is hit
        break
    count += 1

  return retlist

def store_images(vidcap, storage_folder):
  count = 0;
  success = True
  while success:
    success,image = vidcap.read()
    sys.stdout.write(".")
    sys.stdout.flush()
    cv2.imwrite(storage_folder + ("frame%d.jpg")%count, image)     # save frame as JPEG file
    if cv2.waitKey(10) == 27:                     # exit if Escape is hit
        break
    count += 1

if __name__ == "__main__":
  # Parse arguments
  parser = argparse.ArgumentParser()
  setup_arg_parser(parser)
  args = parser.parse_args()

  # Store arguments into variables
  input_mp4 = args.input_mp4
  storage_folder = args.output_folder

  if not os.path.exists(storage_folder):
    os.makedirs(storage_folder)
  vidcap = cv2.VideoCapture(input_mp4)
  
  print type(vidcap)
  store_images(vidcap, storage_folder)
  # target_data = get_target_data_from_video(vidcap, np.array([80,80,100]), np.array([255,255,255]))

  # # gwindow = UI.ImageWindow(frames_dirpath, desired_points)
  # # pointdict = gwindow.retval()

  # for im, md in target_data:
  #   sys.write(".")
  #   cv2.imwrite(storage_folder + ("frame%d.jpg")%count, image)     # save frame as JPEG file

