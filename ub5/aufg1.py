'''
1. 8x8 grosses Teilbild extrahieren (ROI)
2. berechne Kernel fuer jeden Pixel im Teilbild (ROI)
3. berechne Winkel des Vektors
4. trage in Histogramm ein

Zelle = 8x8 Pixel
Block = 2x2 zellen

for each cell in block:
    h = hist(cell)

'''

import cv2
import numpy as np
from math import sqrt
from math import pi

def dot(v1,v2):
    r = 0
    for i in range(len(v2)):
        r += v1[i]*v2[i];
    return r;

def vlen(v):
    r = 0
    for i in v:
        r += i**2
    #print r
    return sqrt(r)

def multk(img, kernel):
    width = len(img[0])
    height = len(img)
    result = np.zeros((height,width), np.int8)
    for x in range(width):
        for y in range(height):
            for i in range(len(kernel[0])):
                for j in range(len(kernel)):
                    imgval = img[x - i][ y - j]
                    if(i > x):
                        x = i
                    if(j > y):
                        y = j
                    #print "img[" + str(x) + " -  " + str(i) + "][ " + str(y) + " - " + str(j) + "]= " + str(imgval)
                    result[x][y] += kernel[i][j] * imgval
    return result;

def angle(v):
    e1 = [1,0]
    #print v
    return dot(v,e1) / (vlen(v) * vlen(e1))

def rag2deg(a):
    return a*180/pi

def isZero(v):
    for i in range(len(v)):
        if(v[i] != 0):
            return False
        return True

def imShow(img, title="image"):
    cv2.imshow(title,img)
    cv2.waitKey(0)

def hist(cell):
    kernel_x = np.array([[-1 , 0 , 1], [-2 ,0 ,2] , [-1 , 0 , 1]])
    kernel_y = np.transpose(kernel_x)

    dst_y = multk(cell, kernel_y)
    dst_x = multk(cell, kernel_x)
    print dst_x
    print dst_y

    sx = len(dst_y)
    sy = len(dst_y[0])
    hist = {}
    for x in range(sx):
        for y in range(sy):
            vec = [dst_x[y][x] , dst_y[x][y]]
            if(not isZero(vec)):
                a = rag2deg(angle(vec)) % 180
                key = a // 20
                print str(vec) + " " + str(key)
                if key in hist:
                    hist[key] += 1
                else:
                    hist[key] = 1
    return hist

img = cv2.imread('people.png',0)
cell = img[0:8, 0:8]
#cv2.imwrite("foo.png",cell)
hist = hist(cell)
print hist
