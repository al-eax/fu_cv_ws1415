#this solution uses pil lib

from PIL import Image

def getChanel(img,channel):
	img = img.convert("RGB")
	subimage = Image.new("RGB", img.size)
	for x in range(img.size[0]):
		for y in range(img.size[1]):
			r = 0
			g = 0
			b = 0
			if channel == "R":
				r = img.load()[x,y][0]
			elif channel == "G":
				g = img.load()[x,y][1]
			elif channel == "B":
				b = img.load()[x,y][2]
			subimage.load()[x, y] = (r,g,b)
	return subimage
	

img = Image.open("image.jpg")
channel = getChanel(img, "R")
channel.show()

