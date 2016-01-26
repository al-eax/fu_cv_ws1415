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

def getGaussians(img, scales = 4):
    #TODO convert to float ?
    result = []
    kernelSize = (9,9)
    for i in range(scales):
        sigma = pow(math.sqrt(2),i)
        print sigma
        blur = img.copy()
        cv2.GaussianBlur(src=img,dst = blur,ksize=kernelSize,sigmaX=sigma,sigmaY=sigma,borderType = cv2.BORDER_DEFAULT )
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

def showDog(dog):
    for d in dog:
        imShow(d,"DOG")

def halveImg(img):
    scale = (len(img)/2, len(img[0])/2)
    return cv2.resize(img,scale, interpolation = cv2.INTER_LINEAR)

def getDOGPyramid(img, octaves = 4):
    k = 0
    for i in range(octaves -1):
        g = getGaussians(img)
        #showGaussians(g)
        dog = getDOG(g)
        showDog(dog)
        img = halveImg(img)

img = cv2.imread("Lenna.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#convert to float64?
getDOGPyramid(img)
