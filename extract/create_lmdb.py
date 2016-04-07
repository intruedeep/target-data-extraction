#!/usr/bin/env python2

import os
import cv2
import sys
import shutil
import numpy as np

RED_LOWER = np.array([0, 0, 100])
RED_UPPER = np.array([80, 80, 200])  
PXL_THRESHOLD = 29
HEIGHT = 720
WIDTH = 1280
PXLS_PER_TILE = 18*32
MAPSIZE = 720*1280*3*22000

def run(infile, imgroot, listfile):
  """ 
      Combines code from image.py, findRed.py and 
      http://deepdish.io/2015/04/28/creating-lmdb-in-python/ to generate a
      database of tiles and mappings to 0 or 1. 0 means no red was in the tile, 1
      means at least 29 red pixels. 
  """
  try:
    vc = cv2.VideoCapture(infile)
  except:
    print("Can't open video file")
    return 0

  count = 0
  while True:
    _, img = vc.read()
    if img is None: break
    try:
      target_tiles(count, img, imgroot, listfile)
    except:
      print("run {} failed".format(count))
    count += 1
  return count
  #print("count = {}".format(count))

def target_tiles(itr, img, imgroot, listfile):
  tr = 40
  tc = 40
  N = tr * tc
  for i in range(0, HEIGHT, tr):
    for j in range(0, WIDTH, tc):
      subi = img[i:i+tr,j:j+tc]
      iso = cv2.inRange(subi, RED_LOWER, RED_UPPER)
      pxls = len(np.flatnonzero(iso))
      locof = tr*(i/tc)+(j/tc)
      ofn = "tile_{}.jpg".format(itr*N+locof)

      # save tile image
      imgfn = os.path.join(imgroot, ofn)
      cv2.imwrite(imgfn, subi)

      # write associated classification to target_train_set.txt
      if pxls > PXL_THRESHOLD:
        liststr = "{} {}\n".format(ofn, 1)
      else:
        liststr = "{} {}\n".format(ofn, 0)
      with open(listfile, 'a') as lf:
        lf.write(liststr)


if __name__ == '__main__':
  """
      Credit to the following sources:
      http://stackoverflow.com/questions/31427094/guide-to-use-convert-imageset-cpp
  """
  if len(sys.argv) < 2:
    print("./create_lmdb.py [video|framedir]")
    print("  Generates tiles and 0/1 mappings for caffe and")
    print("  calls caffe/build/tools/convert_imageset to build lmdb.")
    print("  This code will wipe the current target-train-tiles/ directory")
    print("  and target-train.txt file")
    raise SystemExit

  vidfile = sys.argv[1]
  trainimgs = "/home/utk/Templates/target-train-tiles"
  listfile = "/home/utk/Templates/target-train.txt"
  dbname = "/home/utk/Templates/target-train-lmdb"
  lmdbexec = "/home/utk/caffe/build/tools/convert_imageset --check_size"

  os.system("rm -rf {} {}".format(trainimgs, dbname))
  print(os.listdir('/home/utk/Templates'))
  os.remove(listfile)
  os.mkdir(trainimgs)
  #os.mkdir(dbname)

  # get tiles and classifications from video, the call convert_imageset
  rv = run(vidfile, trainimgs, listfile)
  cmd = "GLOG_logtostderr=1 {} {}/ {} {}".format(lmdbexec, trainimgs, listfile, dbname)
  print(cmd)
  os.system(cmd)
  print("commited {} frames to lmdb".format(rv))
