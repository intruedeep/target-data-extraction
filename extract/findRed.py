#! /usr/bin/python

import numpy as np
from PIL import Image
import sys
import Image
import os

redThreshold = 140
greenThreshold = 80
blueThreshold = 80
pixelThreshold = 1
	
pixelCount = 0

trainList = open('imageList.txt', 'w')

files_in_dir = os.listdir('tiles')
for file_in_dir in files_in_dir:
	img = Image.open('tiles/' + file_in_dir)
	window = np.array(img)
	imgHeight = window.shape[0]
	imgWidth = window.shape[1]
	pixelCount = 0
	for i in range(0, imgHeight):
		for j in range(0, imgWidth):
			if ( window[i][j][0] > redThreshold and window[i][j][1] < greenThreshold and window[i][j][2] < blueThreshold ):
				pixelCount += 1

	if ( pixelCount > pixelThreshold ):
		trainList.write('tiles/' + file_in_dir + ' ' + '1' + "\n")
	else:
		trainList.write('tiles/' + file_in_dir + ' ' + '0' + "\n")

trainList.close()	
