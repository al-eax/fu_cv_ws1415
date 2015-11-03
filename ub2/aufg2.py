import csv
import sys 
import Image

#read csv file
def csv2points(path):
	f = open(path, 'rb')
	reader = csv.reader(f)
	x = []
	y = []
	z = []
	i = 0;
	for row in reader:
		for col in row:
			if i == 0:
				x.append(float(col))
			if i == 1:
				y.append(float(col))
			if i == 2:
				z.append(float(col))
		i = i +1
	points = []
	for p in range(len(x)):
		points.append((x[p],y[p],z[p]))
	return points 

#world to screen by pinhole peojection
def w2cPinhole(point, f):
	factor = float(f)/float(point[2])
	y = factor * point[1]
	x = factor * point[0]
	return (x,y)

def w2cParallel(point, zoom):
	return (point[0]*zoom,point[1]*zoom)

#calculate bounding box
def getBB(points):
	minx = points[0][0]
	miny = points[0][1]
	maxx = points[0][0]
	maxy = points[0][1]

	for point in points:
		if point[0] > maxx:
			maxx = point[0]
		if point[0] < minx:
			minx = point[0]
		if point[1] > maxy:
			maxy = point[1]
		if point[1] < miny:
			miny = point[1]
	return ( (minx,miny,) , (maxx,maxy))

#project 2d points on image
def coords2img(screenCoords,rgb):
	#calc bounding box
	((minx, miny), (maxx, maxy)) = getBB(screenCoords)
	imgSize = (int((maxx - minx) + 1) , int((maxy - miny) + 1))
	img = Image.new( 'RGB',imgSize , "black")
	pixels = img.load()
	#set pixels
	for (px,py) in screenCoords:
		pixel = (int(px - minx ), int(py - miny))
		pixels[pixel] = rgb
	return img


############ 1. img
#read 3d points from csv
points = csv2points("pointdata_3d.csv")
screenCoords = []
f = 10000.0
#convert 3d to 2d
for point in points:
	screenCoords.append(w2cPinhole(point,f))
#display 2d points

img1 = coords2img(screenCoords, (255,0,0))
img1.save("img1_f" + str(f) + ".png")

########## 2. img
screenCoords = []
f = f/2.0
for point in points:
	screenCoords.append(w2cPinhole(point,f))
img2 = coords2img(screenCoords, (0,255,0))
img2.save("img2_f" + str(f) + ".png")


########## 3. img
f = f*2.0
for point in points:
	screenCoords.append(w2cPinhole(point,f))
img3 = coords2img(screenCoords, (0,0,255))
img3.save("img3_f" + str(f) + ".png")

######## parallel projection
screenCoords = []
for point in points:
	screenCoords.append(w2cParallel(point,100))
img4 = coords2img(screenCoords, (0,0,255))
img4.save("img4parallel.png")
