from PIL import Image

def getSubImg(img, x, y, width, height):
	subimage = Image.new("RGBA", (width, height))
	for i in range(x, x+width):
		for j in range(y, y+height):
			subimage.load()[i - x, j - y] = img.load()[i,j]
	return subimage

img = Image.open("image.jpg")
subimg = getSubImg(img, 50,100,60,60)
subimg.show()
subimg.save("aufg12.png")
