import numpy as np
import cv2
from WrappedImage import WrappedImage
from PIL import ImageDraw

def getRange(hsvvect,lowOffset,highOffset):
	#Returns the boundaries of a given 1 tuple element hsv vector.

	lowbounds = np.array([hsvvect[0][0][0] + lowOffset[0], 
						hsvvect[0][0][1] + lowOffset[1], 
						hsvvect[0][0][2] + lowOffset[2]])

	highbounds = np.array([hsvvect[0][0][0] + highOffset[0], 
						hsvvect[0][0][1] + highOffset[1], 
						hsvvect[0][0][2] + highOffset[2]])

	return (lowbounds, highbounds)

class Filter(object):
	def __init__(self, species):
		self.spec_dict = {
			"Isolate": self._get_isolated,
			"None": self._get_none,
			"Pinpoint": self._get_pinpoint
		}

		try:
			self.spec_dict[species]
			self.species = species
		except IndexError:
			raise IndexError("%s is not (currently) a Filter." % (species))

	def get_filtered(self, w_image, argdict):
		return self.spec_dict[self.species](w_image, argdict)

	def _get_isolated(self, w_image, kwargs):
		rgbvect, lowoffset, highoffset = None, None, None
		rgbvect = kwargs["rgbvect"]
		lowoffset = kwargs["lowoffset"]
		highoffset = kwargs["highoffset"]
		if not rgbvect or not lowoffset or not highoffset:
			raise RuntimeError("Not enough arguments provided.")

		temp = np.ndarray((1, 1, 3), np.uint8)
		temp[0][0] = [rgbvect[2], rgbvect[1], rgbvect[0]]

		bgrvect = temp

		#convert bgr vector to hsv
		hsvvect = cv2.cvtColor(bgrvect, cv2.COLOR_BGR2HSV)

		lowbounds, highbounds = getRange(hsvvect, lowoffset, highoffset)

		img = cv2.imread(w_image.image_path)

		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		iso = cv2.inRange(img_hsv, lowbounds, highbounds)

		return WrappedImage(nparray=iso)

	def _get_pinpoint(self, w_image, kwargs):
		x = kwargs["x"]
		y = kwargs["y"]

		new = w_image.pil_image.copy()

		drawing = ImageDraw.Draw(new)

		drawing.ellipse(x, y, y-1,y+1)

		del drawing

		return WrappedImage(nparray="stuff")

	def _get_none(self, w_image, kwargs):
		return w_image
