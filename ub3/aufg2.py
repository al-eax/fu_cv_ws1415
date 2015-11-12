from PIL import Image
import numpy, cv2

def rgb2hsv(rgb):
    (R,G,B) = rgb
    H = S = V = 0.0
    R = float(R / 255.0)
    G = float(G / 255.0)
    B = float(B / 255.0)

    MIN = min(R,G,B)
    MAX = max(R,G,B)


    if MIN == MAX:
        H = 0
    elif MAX == R:
        H = 60.0 * (G - B) / (MAX - MIN)
    elif MAX == G:
        H = 60.0 * (2.0 + (B - R) / (MAX - MIN))
    elif MAX == B:
        H = 60.0 * (4.0 + (R - G) / (MAX - MIN))
    if H < 0.0:
        H += 360.0

    if MAX == 0:
        S = 0
    else:
        S = (MAX - MIN)/MAX
    V = MAX
    return (H,S,V)

def hsvhist(img):
    resut = []
    d = {}
    i = img.load()
    #result = Image.new("RGB", img.size)
    #o = result.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            (H,S,V) = rgb2hsv(i[x,y])
            H = int(H)
            if H in d:
                d[H] += 1
            else:
                d[H] = 1
    return d

def getImgMoment(img, i,j):
	s = 0
	for x in range(img.size[0]):
		for y in range(img.size[1]):
			s += x**i * y**j * img.load()[x,y]
	return s

# convert opencv video frame to pil image
def cv2pil(frame):
	cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	pil_im = Image.fromarray(cv2_im)
	return pil_im

def getFrame(file, n):
	frame = 0
	for i in range(n):
		cam = cv2.VideoCapture(file)
		if cam.grab():
			flag, frame = cam.retrieve()
	return frame



def getImgProb(hist, img):
	result = []
	totalSum = 0
	for value in hist.values():
		totalSum += value

	for x in range(img.size[0]):
		line = []
		for y in range(img.size[1]):
			(H,S,V) = rgb2hsv(img.load()[x,y])
			H = int(H)
			pixelProp = 0.0
			if H in hist:
				pixelProp = float(hist[H]) / float(totalSum)
			else:
				#print "fuck " + str(H)
				pass
			line.append(pixelProp)
		result.append(line)
	return result

def imgProb2Gray(prob):
	width = len(prob[0])
	height = len(prob)
	img = Image.new("L",(height, width))
	for y in range(height):
		for x in range(width):
			#0 = black = improbable
			#255 = white = probable
			val = int(prob[y][x]*255.0)
			img.load()[y,x] = val
	return img

'''
1. get 100. frame from video
2. convert frame to image
3. read subimage
4. get hue histogramm from subimage
5. get object probability from image by histogramm from subimage
6. convert probability
'''

file = "racecar.avi"
frame = getFrame(file, 2)
img = cv2pil(frame)

subimg = Image.open("subsub.png").convert("RGB")

subgimgHist = hsvhist(subimg)

prob = getImgProb(subgimgHist, img)

probimg = imgProb2Gray(prob)
probimg.show()
