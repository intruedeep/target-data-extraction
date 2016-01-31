from PIL import Image
from ImageTkDupe import PhotoImage

class WrappedImage(object):
	def __init__(self, **kwargs):
		if len(kwargs) > 1:
			raise RuntimeError("Too many arguments.")

		if kwargs.keys()[0] == "imgpath":
			imgpath = kwargs[kwargs.keys()[0]]
			self.image_path = imgpath
			self.pil_image = Image.open(self.image_path)
			self.tk_image = PhotoImage(self.pil_image)
			#self.im_type = im_type
		elif kwargs.keys()[0] == "nparray":
			self.image_path = None
			self.pil_image = Image.fromarray(kwargs["nparray"])
			self.tk_image = PhotoImage(self.pil_image)
			#self.im_type = 

		elif kwargs.keys()[0] == "pil_image":
			self.image_path = None
			self.pil_image = kwargs[kwargs.keys()[0]]
			self.tk_Image = PhotoImage(self.pil_image)
		else:
			raise RuntimeError("This kwarg is not currently supported.")
