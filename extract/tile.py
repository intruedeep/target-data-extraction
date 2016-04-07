#! /usr/bin/env python

from PIL import Image
#import Image
import sys
import os
import time

def tile(frame, height, width, dCounter):
		im = Image.open('frames/' + frame)
		tmp = frame.replace('frame', '')
		frameNum = tmp.replace('.jpg', '')
		imgwidth, imgheight = im.size
		counter = 0
		for i in range(0, imgheight, height):
				for j in range(0, imgwidth, width):
						box = (j, i, j+width, i+height)
						a = im.crop(box)
						a.save('tiles/tiles' + str(dCounter) + '/frame' + frameNum + '_tile' + str(counter) + '.jpg')
                                                a.close()
						counter += 1
                im.close()

files_in_dir = os.listdir('frames')
fileCounter = 0
directoryCounter = 0

newpath = 'tiles/tiles' + str(directoryCounter)
if not os.path.exists(newpath):
        os.makedirs(newpath)

oldtime = time.clock()

for file_in_dir in files_in_dir:
	tile(file_in_dir, 18, 32, directoryCounter)
        if ( fileCounter % 300 == 0 ):
            directoryCounter += 1
            newpath = 'tiles/tiles' + str(directoryCounter)
            if not os.path.exists(newpath):
                    os.makedirs(newpath)

        if ( fileCounter % 100 == 0 ):
            nowish = time.clock()
            delta = nowish - oldtime
            oldtime = nowish
            print str(fileCounter) + " time:" + str(delta)


        if ( fileCounter == 22500 ):
            break
        fileCounter += 1
