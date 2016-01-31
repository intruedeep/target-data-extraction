import Tkinter
from Tkinter import BooleanVar
from PIL import Image
import ImageTkDupe
import Pmw
import Utils
from Utils import path_by_dir_index
from pylab import imshow, show, imread
import os
from Filter import Filter
from WrappedImage import WrappedImage
from copy import copy

#TODO update this>>>> Window that shows the given image, and returns user-specified pinpoints
class ImageWindow():
	def __init__(self, frames_dirpath, seven_segment_num):
		self.root = Tkinter.Tk()
		self.root.resizable(0,0)
		self.frames_dirpath = frames_dirpath

		self.boundtypetuple = ("low","high")
		self.boundnametuple = ("hue","saturation","value")
		self.bounds = dict()

		#each pps key is the name of a desired pinpoint
		#each value is an rgb value
		self.seven_segment_num = seven_segment_num

		#For use with the checkbox
		decimal_present = BooleanVar()


		self.pps = dict()
		for pp in ppnames:
			self.pps[pp] = (None)


		self.msgBar = Pmw.MessageBar(parent=self.root, entry_width=40, labelmargin=10)
		self.msgBar.label = "Do This:"

		self.curpp = self.pps.keys()[0]

		self.msgBar.message("state", "Selecting %s Color." % (self.curpp))

		#if I'd started out differently I'd use a class structure here... but oh well.
		self.offChooseCmd = dict()
		self.offsetChoose = dict()
		self.selected_color_canvas = dict()
		self.pinpointAdjust = dict()
		self.selected_color_image = dict()
		self.select_which_pp_button_dict = dict()
		self.select_which_pp_cmd_dict = dict()
		self.selected_color_image_dict = dict()

		self.pinpointAdjustFrame = Tkinter.Frame(self.root)

		for pp in ppnames:
			self.pinpointAdjust[ppno] = Tkinter.Frame(self.pinpointAdjustFrame)
			self.pinpointAdjust[ppno].grid(row=0,column=ppno)
		

		boundtypeno = 0
		for boundtype in self.boundtypetuple:
			for boundname in self.boundnametuple:
				ktuple = (pp, boundtype, boundname)

				if boundtype == "low":
					self.bounds[ktuple] = -10
				elif boundtype == "high":
					self.bounds[ktuple] = 10

				self.offChooseCmd[ktuple] = self.getOfstChooseCmd(ktuple)
				self.offsetChoose[ktuple] = Pmw.EntryField(parent=self.pinpointAdjust[ppno],
														command=self.offChooseCmd[ktuple],
														value=self.bounds[ktuple],
														labelpos='w',
														label_text="%s %s %s offset" % ktuple)	

				self.offsetChoose[ktuple].label = (pp + " " + boundname)
				self.offsetChoose[ktuple].grid(row=boundtypeno)

				boundtypeno += 1

			self.select_which_pp_cmd_dict[pp] = self.select_which_pp_cmd_wrapper(pp)
			self.select_which_pp_button_dict[pp] = Tkinter.Button(self.pinpointAdjust[ppno],
																text="Select %s Reference Pixel" %(pp),
																command=self.select_which_pp_cmd_dict[pp])

			self.selected_color_canvas[pp] = Tkinter.Canvas(self.pinpointAdjust[ppno],
															width=50, height = 50)
			
			self.selected_color_canvas[pp].grid(column=1, row=0, rowspan=6)
			self.select_which_pp_button_dict[pp].grid(column=0, row = 7)

		lowbounds, highbounds = self.get_bounds(self.curpp)

		filter_tupe = 	(Filter("Isolate"), 
							{
							"rgbvect": (0,0,0),
							"lowoffset": lowbounds,
							"highoffset": highbounds
							}
						)

		self.img_browser = DirImageBrowser(self.root, self.frames_dirpath, 
											self.gather_pp_info, msgfnc=self.set_msgbar,
											filter_tupe=filter_tupe)

		self.finalize_button = Tkinter.Button(self.root,
												text="Finalize Selections / Begin Analysis",
												command=self.finalize_selection_cmd)
		self.finalize_button.pack()
		self.msgBar.pack()
		self.pinpointAdjustFrame.pack()
		self.img_browser.pack()
		self.root.mainloop()


	#=========================================================
	#	Tkinter Cmds
	#=====================================================

	def getOfstChooseCmd(self, ktuple):
		#A nested workaround for the pmw command restrictions
		#TODO clean up so it doesn't rewrite whole batch whenever it has to change one value
		def realOfstChooseCmd():
			self.set_filter_bounds()
			self.img_browser.set_filter(True)
		return realOfstChooseCmd

	
	def show_iso_cmd_wrapper(self, pp):
		#Another nested workaround for the pmw command restrictions.
		#NOTE: Is currently referenced by more than just show iso button. Be careful.
		def show_iso_cmd():
			if not self.pps[pp] == (None):
				lowbound, highbound = self.get_bounds(self.pps[pp])

			else:
				self.msgBar.message("help","First select %s reference point!" % (pp))
		return show_iso_cmd


	def select_which_pp_cmd_wrapper(self, ppname):
		#The nesting is, again, just a workaround.
		def select_which_pp_cmd():
			self.curpp = ppname
			if not self.pps[self.curpp]:
				self.img_browser.filter_tupe[1]["rgbvect"] = (0 ,0 ,0)
			else:
				self.img_browser.filter_tupe[1]["rgbvect"] = self.pps[self.curpp]
			self.set_filter_bounds()
			self.msgBar.message("state", "Selecting %s Color." % (self.curpp))
		return select_which_pp_cmd


	def finalize_selection_cmd(self):
		for pp in self.pps:
			if self.pps[pp] == None:
				self.msgBar.message("help", "Pinpoint %s was not chosen!" % pp)
				return

		#Save the data gathered 
		#(because we won't be able to access it after window's gone)
		#and then destroy the window.
		self.returndict = dict()
		for pp in self.pps:
			lowbound, highbound = self.get_bounds(pp)
			self.returndict[pp] = (self.pps[pp], lowbound, highbound)
		self.root.destroy()
		return

	def set_msgbar(self, string):
		self.msgBar.message("state", string)

	def gather_pp_info(self, pixel):
		self.pps[self.curpp] = pixel
		self.img_browser.filter_tupe[1]["rgbvect"] = self.pps[self.curpp]
		self.canvas_one_color(self.pps[self.curpp], self.selected_color_canvas[self.curpp])
		self.selected_color_canvas[self.curpp].grid(column=1, row=0, rowspan=6)

	def canvas_one_color(self, rgbtupe, canvas):
		#Takes an rgbtuple, width, height, and tkinter.canvas object, 
		#and creates an image of one color that is painted on canvas
		color = Image.new("RGB", 
							(canvas.winfo_height(), canvas.winfo_width()), 
							"rgb(%s, %s, %s)" % (rgbtupe[0],rgbtupe[1],rgbtupe[2]))
		self.selected_color_image_dict[self.curpp] = ImageTkDupe.PhotoImage(color)
		canvas.create_image(0, 0, image=self.selected_color_image_dict[self.curpp])

	def get_bounds(self, pp):
		lowbound = (int(self.offsetChoose[(pp, "low", "hue")].getvalue()), 
					int(self.offsetChoose[(pp, "low", "saturation")].getvalue()),
					int(self.offsetChoose[(pp, "low", "value")].getvalue()))

		highbound = (int(self.offsetChoose[(pp, "high", "hue")].getvalue()), 
					int(self.offsetChoose[(pp, "high", "saturation")].getvalue()),
					int(self.offsetChoose[(pp, "high", "value")].getvalue()))

		return (lowbound, highbound)


	def set_filter_bounds(self):
		lowbounds, highbounds = self.get_bounds(self.curpp)
		self.img_browser.filter_tupe[1]["lowoffset"] = lowbounds
		self.img_browser.filter_tupe[1]["highoffset"] = highbounds

	#return info gathered.
	def retval(self):
		return self.returndict


#My small version of a pmw megawidget.
#TODO make it so that this doesn't encapsulate filters. 
#I don't like it. Instead, let the outer object deal with that,
#Since it has access to the inner object's image
class DirImageBrowser(object):
	def __init__(self, parent, frames_dirpath, clickfnc, msgfnc=None, filter_tupe=(None, None), reqret="pixel"):
		self.parent = parent
		self.frames_dirpath = frames_dirpath
		self.reqret = reqret

		self.image_index = 0


		self.image = WrappedImage(imgpath=path_by_dir_index(frames_dirpath, self.image_index))
		self.frame = Tkinter.Frame(self.parent)
		self.clickfnc = clickfnc
		self.msgfnc = msgfnc



		width, height = self.image.pil_image.size

		self.filtered_status = False
		self.filter_tupe = filter_tupe#filter for each different iso layer
		
		"""
		Tuple(
			1:Filter object with method get_filtered(w_image=WrappedImage(), args).
				This method is used to get filtered version of given wrappedimage.,
			2:Dict of arguments for get_filtered
		)
		"""


		self.canvas = Tkinter.Canvas(self.frame, width=width, height=height)
		self.canvas.bind("<Button-1>", self._get_click)
		self.canvas.create_image(0, 0, image=self.image.tk_image, anchor = "nw")

		self.img_ctrl_bar = Tkinter.Frame(self.frame)
		self.show_last_img_button = Tkinter.Button(self.img_ctrl_bar,
													text="Show Previous Image",
													command=self.show_last_img_cmd)
		self.show_next_img_button = Tkinter.Button(self.img_ctrl_bar,
													text="Show Next Image",
													command=self.show_next_img_cmd)
		self.toggle_filtered_img_button = Tkinter.Button(self.img_ctrl_bar,
													text="Toggle Filter",
													command=self.toggle_filtered_img_cmd)
		self.img_number_entry = Pmw.EntryField(parent=self.img_ctrl_bar,
												command=self.img_number_entry_cmd,
												value=self.image_index)
		
		self.show_last_img_button.grid(row=0,column=0)
		self.show_next_img_button.grid(row=0,column=4)
		self.toggle_filtered_img_button.grid(row=0,column=3)
		self.img_number_entry.grid(row=0,column=1)

		self.img_ctrl_bar.pack()
		self.canvas.pack()


	#==============================
	#	CMDS
	#=============================

	def show_last_img_cmd(self):
		self.set_img_by_index(self.image_index - 1)

	def show_next_img_cmd(self):
		self.set_img_by_index(self.image_index + 1)
		

	def img_number_entry_cmd(self):
		self.set_img_by_index(int(self.img_number_entry.getvalue()))

	def toggle_filtered_img_cmd(self):
		if self.filter_tupe:
			self.toggle_filter()
		else:
			self.msgfnc("No filter selected.")


	#=====================================
	#	other Fcns
	#===================================


	def set_img_by_index(self, new_index):
		try:
			#store old image just in case this fails...
			self.old_image = copy(self.image)

			self.image = WrappedImage(imgpath=path_by_dir_index(self.frames_dirpath, self.image_index))
			self.canvas.create_image(0, 0, image=self.image.tk_image, anchor = "nw")
			self.image_index = new_index
			self.img_number_entry.setvalue(self.image_index)
			if self.filtered_status == True:
				self.set_filter(True)
		except IndexError as e:
			self.msgfnc(str(e))
			self.image = self.old_image

	def _show_filtered_img(self):
		self.filtered_img = self.filter_tupe[0].get_filtered(self.image, self.filter_tupe[1])
		self.canvas.create_image(0, 0, image=self.filtered_img.tk_image, anchor="nw")

	def _show_unfiltered_img(self):
		self.canvas.create_image(0, 0, image=self.image.tk_image, anchor="nw")
		self.canvas.pack()
		self.filtered_status = False

	def toggle_filter(self):
		self.set_filter(not self.filtered_status)

	def set_filter(self, boolean):
		if boolean:
			self._show_filtered_img()
			self.filtered_status = True
		else:
			self._show_unfiltered_img()
			self.filtered_status = False

	def _get_click(self, event):
		if self.reqret == "pixel":
			if not self.filtered_status:
				pixel = self.image.pil_image.getpixel((event.x,event.y))
				self.clickfnc(pixel)
		if self.reqret == "xy":
			self.clickfnc(event.x, event.y)

	def pack(self):
		self.frame.pack()

	def grid(self, row=0,column=0):
		self.frame.grid(row, column)


#TODO remove the "toggle filter" button from the dirbrowser.
class FindTubeWindow(object):
	def __init__(self, return_list, frames_dirpath):
		self.root = Tkinter.Tk()
		self.frames_dirpath = frames_dirpath
		self.return_list = return_list

		self.limits = [0, 0, 0, 0]
			#(left, right, top, bottom)
		self.cur_select = 0
		self.selection_names = ("Left Boundary", "Right Boundary", 
								"Top Boundary", "Bottom Boundary")


		#Declare major TK widgets
		self.img_browser = DirImageBrowser(self.root,
											frames_dirpath=self.frames_dirpath,
											clickfnc=self.get_point,
											reqret="xy")
		self.msg_bar = Pmw.MessageBar(parent=self.root, 
									entry_width=40, 
									labelmargin=10)
		self.finalize_button = Tkinter.Button(self.root,
										text="Finalize Selections",
										command=self.finalize_command)

		#Set the initial message.
		self.msg_bar.message("state", "Selecting %s" % (self.selection_names[0]))

		#Pack all the widgets.
		self.img_browser.pack()
		self.msg_bar.pack()
		self.finalize_button.pack()
		self.root.mainloop()

	def get_point(self, x, y):
		self.set_bound(self.cur_select, x, y)
		if self.cur_select == 3:
			self.cur_select = 0
		else:
			self.cur_select += 1

		self.msg_bar.message("state", "Selecting %s" % (self.selection_names[self.cur_select]))

	def set_bound(self, index, x, y):
		if index > 1:
			self.limits[index] = y
			self.draw_line("horizontal", y)
		else:
			self.limits[index] = x
			self.draw_line("vertical", x)

	def draw_line(self, orientation, distance):
		width, height = self.img_browser.image.pil_image.size
		if orientation == "horizontal":
			self.img_browser.canvas.create_line(
				0, distance, width, distance)

		elif orientation == "vertical":
			self.img_browser.canvas.create_line(
				distance, 0, distance, height)

	def finalize_command(self):
		for ind in range(4):
			self.return_list[ind] = self.limits[ind]

		print "RETURN LIST:", self.return_list

		self.root.destroy()

class CropImage(object):
    pass


class CalibrationWindow(object):
	def __init__(self, return_list, frames_dirpath, selection_names):
		self.root = Tkinter.Tk()
		self.frames_dirpath = frames_dirpath
		self.return_list = return_list

		self.cur_select = 0
		self.selection_names = selection_names


		#Declare major TK widgets
		self.img_browser = DirImageBrowser(self.root,
											frames_dirpath=self.frames_dirpath,
											clickfnc=lambda x, y:x,
											reqret="xy")
		self.msg_bar = Pmw.MessageBar(parent=self.root, 
									entry_width=40, 
									labelmargin=10)
		self.finalize_button = Tkinter.Button(self.root,
										text="Finalize Selections",
										command=self.finalize_command)
		self.enterval_field = Pmw.EntryField(self.root,
											command=self.enterval_field_cmd)

		#Set the initial message.
		self.msg_bar.message("state", "Selecting %s" % (self.selection_names[0]))

		#Pack all the widgets.
		self.img_browser.pack()
		self.msg_bar.pack()
		self.finalize_button.pack()
		self.root.mainloop()

	def enterval_field_cmd(self):
		value = self.enterval_field.getvalue()
		self.return_list.insert(self.cur_select, (selection_names[self.cur_select], value))

	def finalize_command(self):
		print "RETURN LIST:  ", self.return_list
		self.root.destroy()



