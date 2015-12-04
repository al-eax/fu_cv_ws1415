import cv2
import numpy as np


def M(img, i,j):
    #https://en.wikipedia.org/wiki/Image_moment#Raw_moments
    width = len(img)
    height = len(img[0])
    result = 0
    for x in range(width):
        for y in range(height):
            result += x**i * y**i*img[x,y]
    return result

def rgb2bin(img):
    #http://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html#gsc.tab=0
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def showImg(img, title="image"):
    cv2.imshow(title,img)
    cv2.waitKey(0)


def centMoment(img, p,q):
    #https://en.wikipedia.org/wiki/Image_moment#Central_moments
    width = len(img)
    height = len(img[0])
    meanx = M(img,1,0)/M(img,0,0)
    meany = M(img,0,1)/M(img,0,0)
    result = 0
    for x in range(width):
        for y in range(height):
            result += (x-meanx)**p * (y-meany)**q * img[x,y]
    return result

def n(img,i,j):
    #https://en.wikipedia.org/wiki/Image_moment#Scale_invariant_moments
    return centMoment(img,i,j) / M(img,0,0)**(1 + (i+j)/2)

def getImoments(img):
    i1 = n(img,2,0) + n(img,0,2)
    i2 = (n(img,2,0) - n(img,0,2))**2 + 4*n(img,1,1)**2
    i3 = (n(img,3,0) - 3*n(img,1,2))**2 + (3*n(img,2,1) + n(img,0,3))**2
    i4 = (n(img,3,0) + n(img,1,2))**2 + (n(img,2,1) + n(img,0,3))**2
    i5 = (n(img,3,0) - 3*n(img,1,2))*(n(img,3,0) + n(img,1,2))*    ((n(img,3,0) + n(img,1,2))**2 - 3*(n(img,2,1) + n(img,0,3))**2)
    i5 += (3*n(img,2,1) - n(img,0,3))*(n(img,2,1)+n(img,0,3)) *    (3*(n(img,3,0)+n(img,1,2)**2) - (n(img,2,1)+n(img,0,3))**2)
    i6 = (n(img,2,0) - n(img,0,2)) * ( (n(img,3,0) + n(img,1,2))**2 - (n(img,2,1) + n(img,3,0))**2 )
    i6 += 4*n(img,1,1)*(n(img,3,0)+n(img,1,2))*(n(img,2,1)+n(img,0,3))
    i7 = (3*n(img,2,1) - n(img,0,3))*(n(img,3,0)+n(img,1,2)) * (   (n(img,3,0)+n(img,1,2))**2 -3*(n(img,2,1)+n(img,0,3)**2))
    i7 -= (n(img,3,0)-3*n(img,1,2))*(n(img,2,1)+n(img,0,3)) * (  3*(n(img,3,0)+n(img,1,2))**2 - (n(img,2,1)+n(img,0,3))  )
    return (i1,i2,i3,i4,i5,i6,i7)

def qdist(m1, m2):
    result = 0
    for i in range(len(m1)):
        result += (m1[i] - m2[i])**2
    return result

img1 = cv2.imread("heystack.png",0)
img2 = cv2.imread("needle.png",0)



bb1 = img1[19 : 75, 9 : 64]
bb2 = img1[36 : 97, 140 : 212]
bb3 = img1[146 : 234 , 35 : 155]
bb4 = img1[96 : 131 , 262 : 310]

mi = getImoments(img2)

dists = [
        qdist(mi,getImoments(bb1)),
        qdist(mi,getImoments(bb2)),
        qdist(mi,getImoments(bb3)),
        qdist(mi,getImoments(bb4))
    ]
print dists
print min(dists)
