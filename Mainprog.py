import TubeReader
import UI
import os
import numpy as np
import cv2
import Utils
import sys
import getopt
import Tkinter
from SevenSegment import SevenSegmentNumber

Button = Tkinter.Tk()
Button.mainloop()

os.chdir("C:\Users\lbechtel\Google Drive\Dropbox\Work Stuff\TubeReader\dev")


class Client(object):
	def __init__(self, frames_dirpath, xl_dirpath, num_digits, window_opt=True, tubewindow_opt=False):
		self.mm_total_height = mm_total_height

		opts, args = getopt.getopt(sys.argv[1:], "u:")

		#Do we need to use windows to select our values, or should we use the defaults?
		self.window_opt = window_opt
		self.tubewindow_opt = tubewindow_opt

		print opts
		for opt in opts:
			print opt
			if opt == "-w":
				window = True


		#Path to get to time lapse frames.
		#frames_dirpath = "C:\\Users\\lbechtel\\Pictures\\TubeReader Shots\\9-27-2013"
		self.frames_dirpath = frames_dirpath


		#Path to excel output directory.
		#xl_dirpath = "C:\\Users\\lbechtel\\Google Drive\\Dropbox\\Work Stuff\\TubeReader\\OutputSheets"
		self.xl_dirpath = xl_dirpath
		

		seven_segment_num = SevenSegmentNumber(num_digits)


		lowbounds = dict()
		highbounds = dict()

		pointdict = dict()


		gwindow = UI.ImageWindow(frames_dirpath, desired_points, )
		pointdict = gwindow.retval()


		rect = [15, 124, 134, 650]
		if tubewindow:
			twindow = UI.FindTubeWindow(rect, frames_dirpath)


		#a dictionary with keys representing desired_points, value tuples of form:
		#((rgbtuple), (lowtolerancehsvtuple), (hightolerancehsvtuple))
		low_hsv_tolerance = dict()
		high_hsv_tolerance = dict()
		for point in pointdict:
			low_hsv_tolerance[point] = pointdict[point][1]
			high_hsv_tolerance[point] = pointdict[point][2]

		pointBGR = dict()

		print pointBGR

		for key in pointdict:
			temp = np.ndarray((1, 1, 3), np.uint8)
			temp[0][0] = [pointdict[key][0][2], pointdict[key][0][1], pointdict[key][0][0]]
			pointBGR[key] = temp

		pointHSV = dict()

		for key in pointBGR:
			pointHSV[key] = cv2.cvtColor(pointBGR[key], cv2.COLOR_BGR2HSV)

		print pointHSV

		for key in pointHSV:
			lowbounds[key], highbounds[key] = Utils.getRange(pointHSV[key], 
															low_hsv_tolerance[key],
															high_hsv_tolerance[key])
			print key, "low", lowbounds[key]
			print key, "high", highbounds[key]


		TubeReader.gatherData(frames_dirpath=frames_dirpath, xl_dirpath=xl_dirpath,
								lowBounds=lowbounds, highBounds=highbounds,
								rect=rect, mm_total_height=self.mm_total_height,
								tube_name=tube_name)


if __name__ == "__main__":
    client = Client(mm_total_height=193.5)




