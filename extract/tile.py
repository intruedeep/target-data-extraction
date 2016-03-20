from PIL import Image
import Image
import sys

def tile(frame, height, width):
		im = Image.open('frames/' + frame)
		tmp = frame.replace('frame', '')
		frameNum = frame.replace('.jpg', '')
		imgwidth, imgheight = im.size
		area = height * width
		counter = 0
		for i in range(0, imgheight, height):
				for j in range(0, imgwidth, width):
						box = (j, i, j+width, i+height)
						a = im.crop(box)
						a.save('tiles/frame' + frameNum + '_tile' + str(counter) + '.jpg')
						counter += 1

files_in_dir = os.listdir('frames')
for file_in_dir in files_in_dir:
	tile(file_in_dir, 18, 32)
