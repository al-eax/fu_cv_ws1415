from PIL import Image

def mirror(img,axis):
	newImg = Image.new("RGB", img.size)
	width, height = img.size
	for x in range(width -1):
		for y in range(height-1):
			if axis == "x":
				newImg.load()[x,y] = img.load()[width - x -1, y]
			if axis == "y":
				newImg.load()[x,y] = img.load()[x,height - y -1]
	return newImg

img = Image.open("image.jpg")
m = mirror(img, "x")
m.show()
m.save("aufg14.png")
