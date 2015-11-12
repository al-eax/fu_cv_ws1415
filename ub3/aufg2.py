from PIL import Image
import numpy, cv2
import colorsys

def rgb2hsv(rgb):
    (R,G,B) = rgb
    H = S = V = 0.0
    R = float(R / 255.0)
    G = float(G / 255.0)
    B = float(B / 255.0)
    return colorsys.rgb_to_hsv(R,G,B)
def hsvhist(img):
    resut = []
    d = {}
    i = img.load()
    #result = Image.new("RGB", img.size)
    #o = result.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            (H,S,V) = rgb2hsv(i[x,y])
            H = int(H*100)
            if H in d:
                d[H] += 1
            else:
                d[H] = 1
    return d


# convert opencv video frame to pil image
def cv2pil(frame):
	cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	pil_im = Image.fromarray(cv2_im)
	return pil_im

def getFrame(file, n):
	frame = 0
	cam = cv2.VideoCapture(file)
	for i in range(n):
		if cam.grab():
			flag, frame = cam.retrieve()
	return frame



def getImgProb(hist, img):
	result = []
	totalSum = 0.0
	for value in hist.values():
		totalSum += value

	for x in range(img.size[0]):
		line = []
		for y in range(img.size[1]):
			(H,S,V) = rgb2hsv(img.load()[x,y])
			H = int(H*100)
			pixelProp = 0.0
			if H in hist:
				pixelProp = float(hist[H]) / float(totalSum)
			else:
				##print "fuck " + str(H)
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

file = "racecar.avi"
framenumber = 1
frame = getFrame(file,framenumber )
img = cv2pil(frame)

img.save("frame" + str(framenumber) + ".png")

subimg = Image.open("sub.png").convert("RGB")

subgimgHist = hsvhist(subimg)

prob = getImgProb(subgimgHist, img)

probimg = imgProb2Gray(prob)
probimg.show()
probimg.save("probimg.png")
