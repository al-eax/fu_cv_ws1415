import csv
import sys 

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


def world2screen(point, f):
	factor = float(f)/float(point[2])
	y = factor * point[1]
	x = factor * point[0]
	return (x,y)

def getBB(points):
	minx = points[0][0]
	miny = points[0][1]
	maxx = points[1][0]
	maxy = points[1][1]

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

points = csv2points("pointdata_3d.csv")
screenCoords = []
f = 5.0
for point in points:
	screenCoords.append(world2screen(point,f))
bb = getBB(screenCoords)
print bb

bb = getBB(points)

