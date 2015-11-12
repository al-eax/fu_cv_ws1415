import Image
import matplotlib.pyplot as plt
import colorsys
import numpy as np

def rgb2hsv(rgb):
    (R,G,B) = rgb
    R = float(R / 255.0)
    G = float(G / 255.0)
    B = float(B / 255.0)
    return colorsys.rgb_to_hsv(R,G,B)

def getSubImg(img, x, y, width, height):
    subimg = Image.new(img.mode, (width,height))
    for i in range(width):
        for k in range(height):
            subimg.load()[i,k] = img.load()[x + i, y + k]
    return subimg

def hsvhist(img):
    resut = []
    d = {}
    i = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            (H,S,V) = rgb2hsv(i[x,y])
            H = int(H*100) 
            if H in d:
                d[H] += 1
            else:
                d[H] = 1
    return d

def saveHist(hist,filename):
    line = []
    maxKey = int(max(hist))
    minKey = int(min(hist))	
    for i in range(minKey,maxKey + 1):
        if i in hist:
            line.append(hist[i])
        else:
            line.append(0)
	plt.clf()
    plt.ylabel("Anzahl Pixel")
    plt.xlabel("Hue")
    plt.bar(range(minKey,maxKey + 1),line)
	#plt.plot(range(minKey,maxKey + 1),line)
    plt.savefig(filename)

img = Image.open("racecar.png")
subimg = getSubImg(img, 460, 260, 660, 360)
#subimg.save("sub.png")
hist = hsvhist(img)
subhist = hsvhist(subimg)
saveHist(hist,"hist1")
saveHist(subhist,"subhist")
