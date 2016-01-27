import csv
import sys
import numpy as np
import cv2
import cv
import math

def imShow(img, title="image"):
    cv2.imshow(title,img)
    cv2.waitKey(0)

def readCSV(path = "corners.cvs"):
    r = []
    f = open(path, 'rb')
    reader = csv.reader(f)
    for row in reader:
        r.append( (int(row[0]) , int(row[1])))
    return r


def getGaussians(img,currentOctave , scales = 4):
    result = []
    #kernelSize = (9,9)
    kernelSize = (5,5)
    sigma = 1.6
    for i in range(scales):
        #TODO beginne mit anderem Sigma !!!!!
        k = pow(math.sqrt(2),i)
        #k = (i+1) * math.sqrt(2)
        blur = img.copy()
        cv2.GaussianBlur(src=img,dst = blur,ksize=kernelSize,sigmaX=sigma*k,sigmaY=sigma,borderType = cv2.BORDER_DEFAULT )
        result.append(blur)
    return result

def getDOG(gaussians):
    result = []
    for i in range(len(gaussians) -1):
        d = gaussians[i+1]  - gaussians[i]
        result.append(d)
    return result

def showGaussians(gaus):
    for g in gaus:
        imShow(g,"Gaussian")

def showDogs(dogs):
    for d in dogs:
        imShow(d,"DOG")

def halveImg(img):
    scale = (len(img)/2, len(img[0])/2)
    return cv2.resize(img,scale, interpolation = cv2.INTER_LINEAR)

def getDOGPyramid(img, octaves = 4):
    k = 0
    dogs = []
    for i in range(octaves -1):
        g = getGaussians(img,i)
        d = getDOG(g)
        dogs.append(d)
        img = halveImg(img)
        #showGaussians(g)
        #showDogs(d)
    return dogs

def getKeyPoints(doglist):
    listOfKeypoints = []
    for dogs in doglist:
        keypoints = []
        d1 = dogs[0]
        d2 = dogs[1]
        d3 = dogs[2]
        final = d1.copy()
        final[:,:] = 100
        for start_y in range(len(d1) - 3):
            for start_x in range(len(d1[0]) - 3):
                minVal = (0,0,0,dogs[0][0][0])
                maxVal = (0,0,0,dogs[0][0][0])
                for x in range(start_x , start_x + 3):
                    for y in range(start_y , start_y + 3):
                        for z in range(3):
                            if (minVal[3] < dogs[z][y][x]):
                                minVal = (z,y,x,dogs[z][y][x])
                            if(maxVal[3] > dogs[z][y][x]):
                                maxVal = (z,y,x,dogs[z][y][x])
                final[maxVal[1]][maxVal[2]] = float(200.0)
                final[maxVal[1]][maxVal[2]] = float(0.0)
        imShow(final)
        listOfKeypoints.append(keypoints)

img = cv2.imread("Lenna.png") #read image
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to gray
img = np.float64(img) #convert to float

dogs = getDOGPyramid(img)
getKeyPoints(dogs)
