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
        d = gaussians[i+1] - gaussians[i]
        result.append(d)
    return result

def showGaussians(gaus):
    for g in gaus:
        imShow(g,"Gaussian")

def showDogs(dogs):
    for d in dogs:
        imShow(d,"DOG")

def halveImg(img):
    scale = (len(img[0])/2, len(img)/2)
    return cv2.resize(img,scale, interpolation = cv2.INTER_LINEAR)

def getDOGLaplacePyramid(img, octaves = 4):
    k = 0
    dogs = []
    gaussians = []
    for i in range(octaves):
        g = getGaussians(img,i)
        gaussians.append(g)
        d = getDOG(g)
        dogs.append(d)
        img = halveImg(img)
        #showGaussians(g)
        #showDogs(d)
    return (gaussians,dogs)

def getKeyPoints(doglist):
    listOfKeypoints = []
    for dogs in doglist:
        keypoints = []
        for start_y in range(len(dogs[0]) - 3):
            for start_x in range(len(dogs[0][0]) - 3):
                d1 = dogs[0][start_y : start_y +3 ,start_x : start_x + 3 ]
                d2 = dogs[1][start_y : start_y +3 ,start_x : start_x + 3 ]
                d3 = dogs[2][start_y : start_y +3 ,start_x : start_x + 3 ]

                middlLoc = (1,1)
                middlVal = d2[1,1]

                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(d1)
                if(minVal > middlVal or maxVal > middlVal):
                    continue
                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(d2)
                if(minVal > middlVal or maxVal > middlVal):
                    continue
                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(d2)
                if(minVal > middlVal or maxVal > middlVal):
                    continue
                add = True
                for x in range(3):
                    for y in range(3):
                        if(d1[y][x] == middlVal):
                            add = False
                        if(not (x == 1 and y == 1) and d2[y][x] == middlVal):
                            add = False
                        if(d3[y][x] == middlVal):
                            add = False
                if(add == True):
                    keypoints.append(((start_x + 1 ,start_y + 1 ),middlVal))
                    #print middlVal
                    #print d1
                    #print d2
                    #print d3
                    #print "------------"
        listOfKeypoints.append(keypoints)
    return listOfKeypoints

def drawKeypoints(img, keypoints,radius = 1):
    for i in range(len(keypoints)):
        for kp in keypoints[i]:
            ((x,y),val) = kp
            center = (x*(2**i) ,y*(2**i))
            print center
            cv2.circle(img,center ,(len(keypoints)-i)*2 , 255)

def deriveImg(img):
    imX = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3) #or cv2.CV_64F ?
    imY = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3) #or cv2.CV_64F ?
    return (imX,imY)

def reject(keypoints, dogs, r = 10.0):
    newKeypoints = []
    for i in range(len(dogs)):
        newDogKeypoints = []
        dog = dogs[i] #diff of gauss
        kps = keypoints[i]
        d2 = dog[0] #get middl dog

        (dx,dy) = deriveImg(d2)
        (dxx,dyx) = deriveImg(dx)
        (dxy,dyy) = deriveImg(dy)

        #print str(len(kps)) + " Keypoints before rejection"
        for kp in kps:
            ((x,y),value) = kp
            if(dx[y][x] < 0.03 and dy[y][x] < 0.03):
                continue
            TrH = float(dxx[y][x]) + float(dyy[y][x])
            DetH = float(dxx[y][x]) * float(dyy[y][x]) - float(dxy[y][x])**2
            if(DetH == 0):
                continue
            if( (TrH**2 / DetH) < ((r+1)/r) ):# < or > ?
                newDogKeypoints.append(kp)
        newKeypoints.append(newDogKeypoints)
        #print str(len(newDogKeypoints)) + " Keypoints after rejection"
        #print "---------"
    return newKeypoints

img = cv2.imread("Lenna.png")#cv2.imread("Lenna.png") #read image
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to gray
o1 = img.copy()
img = np.float64(img) #convert to float

(gaussians,dogs) = getDOGLaplacePyramid(img)
keypoints = getKeyPoints(dogs)

keypoints = reject(keypoints,dogs)
drawKeypoints(o1,keypoints)
imShow(o1)
