import numpy as np
import scipy
import pymorph
from scipy import ndimage
import cv2
import matplotlib
import os
import xlwt
import time
import Utils
from Utils import printPylab, print_center
import re
from math import tan, atan, fabs
from decimal import Decimal


#self.mm_total_height = 193.5

#first_col_width = 30

#todo make it raise errors to the next level function when it catches too many centers
def getCenter(binimg):
	contours, hierarchy = cv2.findContours(binimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if contours:
		cnt = getLargestContour(contours)
		(x,y), radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		return center
	else:
		return None

def getLargestContour(contours=None):
	if contours:
		Areacontours = list()
		largest = 0.0
		lrgInd = None
		for i in range (0, len(contours)):
		    new = cv2.contourArea(contours[i])
		    if (new > largest ):
		    	largest = new
		    	lrgInd = i

		return contours[lrgInd]
	else:
		raise RuntimeError("No arg for getLargestContour")


def get_mapping(px_real_points): #[(px, real)...]
	srt_px_real_points = sorted(px_real_points)

	def mapping(given_px, srt_px_real_points):
		i = 0
		for px, real in srt_px_real_points:
			if given_px == px:
				return float(real)

			elif given_px > px:
				if i == len(srt_px_real_points) - 1:
					m = float(real - srt_px_real_points[i-1][1])/float(px - srt_px_real_points[i-1][0])
					b = float(real - m*px)
					return given_px*m + b
				else:
					if given_px < srt_px_real_points[i+1][0]:
						m = float(srt_px_real_points[i+1][1] - real)/float(srt_px_real_points[i+1][0] - px)
						b = float(real - m*px)
						return given_px*m + b

			elif given_px < px:
				if i == 0:
					m = float(srt_px_real_points[i+1][1] - real)/float(srt_px_real_points[i+1][0] - px)
					b = float(real - m*px)
					return given_px*m + b
				else:
					if given_px > srt_px_real_points[i-1][0]:
						m = float(real - srt_px_real_points[i-1][1])/float(px - srt_px_real_points[i-1][0])
						b = float(real - m*px)
						return given_px*m + b

			i += 1


	return lambda given_px, srt_px_real_points=srt_px_real_points: mapping(given_px, srt_px_real_points)

def getTubeLevel(fname, lowBounds, highBounds, rect, 
				mm_total_height, mm_zero):
	#load image from file
	img = cv2.imread(fname)

	if img == None:
		return "Unread"

	orig_img_height = img.shape[0]


	#Get cropped image dimensions from our rectangle argument
	#So that we don't have as much interference.
	tube_left = rect[0]
	tube_right = rect[1]
	tube_top = rect[2]
	tube_bottom = rect[3]

	#Crop image according to dimensions
	img_crop = img[tube_top:tube_bottom, tube_left:tube_right]


	#convert to hsv
	img_hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)

	#create blurred version of image for easier top detection
	hsv_blur = cv2.GaussianBlur(img, (5, 5), 0)

	#isolate colors
	ball_iso = cv2.inRange(img_hsv, lowBounds["Ball"], highBounds["Ball"])
	top_iso = cv2.inRange(img_hsv, lowBounds["Top"], highBounds["Top"])
	bot_iso = cv2.inRange(img_hsv, lowBounds["Bottom"], highBounds["Bottom"])

	blur_bot = ndimage.gaussian_filter(bot_iso, 8)
	blur_ball = ndimage.gaussian_filter(ball_iso, 8)
	blur_top = ndimage.gaussian_filter(top_iso, 8)

	#Get each part's center in pixels
	if getCenter(blur_ball):
		ball_center = getCenter(blur_ball)

	else:
		print fname, "No Ball found!"
		return "Null"
	if getCenter(blur_top):
		top_center = getCenter(blur_top)
	else:
		print fname, "No Top Reference found!"
		return "Null"
	if getCenter(blur_bot):
		bot_center = getCenter(blur_bot)
	else:
		print fname, "No Bottom Reference Found!"
		return "Null"

	
	#We use the next few bits of info to counteract the pixel distortion 
	#that occurs as we get further from the centerpoint.

	#Px_height between topref and botref
	px_total_height = bot_center[1] - top_center[1]

	mm_over_px = mm_total_height/px_total_height

	ball_height_px = ball_center[1] - top_center[1]

	ball_height_mm = ball_height_px*mm_over_px

	final_answer =  ball_height_mm + mm_zero


	#DESTROY IT!!!

	final_answer = ball_height_px

	return final_answer



#TODO make this sort cleaner c:
def gatherData(frames_dirpath, xl_dirpath, 
				lowBounds, highBounds,
				rect, mm_total_height,fname, col_widths=(30, 10, 10, 10),
				tube_name="UNNAMED"):
	booru_datetime_regexp = ".+-(\d+)_(\d+)_(\d+)\s+(AM|PM).+"

	w = xlwt.Workbook()
	ws = w.add_sheet("Data")

	tlist = dict()

	for photo_fname in os.listdir(frames_dirpath):
		photo_path = os.path.join(frames_dirpath, photo_fname)
		tlist[time.strftime("%m/%d/%Y %H:%M:%S ",
			time.localtime(os.path.getmtime(photo_path)))] = photo_fname
	

	print sorted(tlist)
	sortedlist = list()
	tlistcop = tlist.copy()
	while len(tlist) != 0:
		lowest = min(tlist.keys())
		sortedlist.append((lowest, tlistcop[lowest]))
		del tlist[lowest]

	i = 1
	ws.write(0, 0, "Date")
	ws.write(0, 1, "PX_Calculated")
	ws.write(0, 2, "My Read")
	ws.write(0, 3, "Difference")
	for tupe in sortedlist:
		ws.col(0).width = 256 * col_widths[0]
		ws.write(i, 0, tupe[0])
		ws.write(i, 1, getTubeLevel(os.path.join(frames_dirpath, tupe[1]), lowBounds, highBounds, rect))
		ws.write(i, 3, xlwt.Formula("$B$%d-$C$%d" % (i + 1, i + 1)))
		i += 1

	fname = "Tube %s Read On" % tube_name + time.strftime("%m_%d_%Y At %H_%M_%S ", time.localtime()) + ".xls"
	
	#Save excel sheet.
	w.save(os.path.join(xl_dirpath, fname))


