import Image

def rgb2gray(img):
	width, height = img.size
	for x in range(width -1):
		for y in range(height -1):
			r,g,b = img.load()[x,y]
			g = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
			img.load()[x,y] = (g,g,g)
			
img = Image.open('image.jpg')#.convert('LA')
rgb2gray(img)
img.show()
