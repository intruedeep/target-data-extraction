import re
import os
import numpy as np
import cv2
import pylab
from PIL import Image
import datetime
from Filter import Filter
import Tkinter

def convertFname(fname=None):
	#I don't know what this is.
	if fname == None:
		raise RuntimeError("No argument for convertFname provided.")
	rgx = re.compile("\S+(\d+)\S+")
	match = rgx.match(fname)

	print match[0]

def getRange(hsvvect,lowOffset,highOffset):
	#Returns the boundaries of a given 1 tuple element hsv vector.

	lowbounds = np.array([hsvvect[0][0][0] + lowOffset[0], 
						hsvvect[0][0][1] + lowOffset[1], 
						hsvvect[0][0][2] + lowOffset[2]])

	highbounds = np.array([hsvvect[0][0][0] + highOffset[0], 
						hsvvect[0][0][1] + highOffset[1], 
						hsvvect[0][0][2] + highOffset[2]])

	return (lowbounds, highbounds)

def printPylab(image):
	#Prints a given np.array as an image in pylab.
	pylab.imshow(image)
	pylab.show()

def print_center(coords):
	#Prints given np.array with the coordinates specified circled with a tiny ellipse
	print coords[0], coords[1]


def blend_nparray_images(background, overlay):
	newimg = background.copy()
	opacity = 0.4
	cv2.addWeighted(overlay, opacity, background, 1 - opacity, 0, newimg)
	return newimg

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def get_fname_by_dir_index(dirpath, index):
	try:
		return os.listdir(dirpath)[index]
	except IndexError:
		raise IndexError("File with index %d does not exist in directory \"%s\"." % (index, dirpath))

def path_by_dir_index(parent_dirpath, index):
	return os.sep.join((parent_dirpath, get_fname_by_dir_index(parent_dirpath, index)))



