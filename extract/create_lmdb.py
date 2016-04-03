#!/usr/bin/env python2

import os
import cv2
import sys
import shutil
import numpy as np

class GenDB:

  def __init__(self, infile, udir=None):
    """
        MAPSIZE = width * height * nchannels * maxNumFrames
          22000 was chosen because it's slightly larger than the 21284 frames
          captured from the target-video.webm file. This variable controls the
          max size of the lmdb being created.
    """
    self.infile = infile
    self.udir = udir
    self.imgroot = None
    self.listfile = None
    self.RED_LOWER = np.array([0, 0, 100])
    self.RED_UPPER = np.array([80, 80, 200])  
    self.PXL_THRESHOLD = 29
    self.HEIGHT = 720
    self.WIDTH = 1280
    self.PXLS_PER_TILE = 18*32
    self.MAPSIZE = 720*1280*3*22000

  def run(self, rootfolder, listfile):
    self.imgroot = rootfolder
    self.listfile = listfile
    if self.udir is None:
      return self._run()
    else:
      return self._runFromDir()

  def _run(self):
    """ 
        Combines code from image.py, findRed.py and 
        http://deepdish.io/2015/04/28/creating-lmdb-in-python/ to generate a
        database of tiles and mappings to 0 or 1. 0 means no red was in the tile, 1
        means at least 29 red pixels. 
    """
    try:
      vc = cv2.VideoCapture(self.infile)
    except:
      print("Can't open video file")
      return 0

    count = 0
    while True:
      _, img = vc.read()
      if img is None: break
      try:
        self._target_tiles(count, img)
      except:
        print("run {} failed".format(count))
      count += 1
    return count
    #print("count = {}".format(count))

  def _target_tiles(self, itr, img):
    tr = 40
    tc = 40
    N = tr * tc
    for i in range(0, self.HEIGHT, tr):
      for j in range(0, self.WIDTH, tc):
        subi = img[i:i+tr,j:j+tc]
        iso = cv2.inRange(subi, self.RED_LOWER, self.RED_UPPER)
        pxls = len(np.flatnonzero(iso))
        locof = tr*(i/tc)+(j/tc)
        ofn = "tile_{}.jpg".format(itr*N+locof)

        # save tile image
        imgfn = os.path.join(self.imgroot, ofn)
        cv2.imwrite(imgfn, subi)

        # write associated classification to target_train_set.txt
        if pxls > self.PXL_THRESHOLD:
          liststr = "{} {}\n".format(ofn, 1)
        else:
          liststr = "{} {}\n".format(ofn, 0)
        with open(self.listfile, 'a') as lf:
          lf.write(liststr)

  def _runFromDir(self):
    pass

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
  lmdbexec = "/home/utk/caffe/build/tools/convert_imageset"

  os.system("rm -rf {} {}".format(trainimgs, dbname))
  os.remove(listfile)
  os.mkdir(trainimgs)

  # get tiles and classifications from video, the call convert_imageset
  gdb = GenDB(vidfile)
  rv = gdb.run(trainimgs, listfile)
  cmd = "GLOG_logtostderr=1 {} --resize_height=18 --resize_width=32 {} {} {}".format(lmdbexec, trainimgs, listfile, dbname)
  os.system(cmd)
  print("commited {} frames to lmdb".format(rv))
