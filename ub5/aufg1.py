'''
1. 8x8 grosses Teilbild extrahieren (ROI)
2. berechne Kernel fuer jeden Pixel im Teilbild (ROI)
3. berechne Winkel des Vektors
4. trage in Histogramm ein

Zelle = 8x8 Pixel
Block = 2x2 zellen = 64x64 pixel

for each cell in block:
    h = hist(cell)

'''

import cv2
import numpy as np
from math import sqrt
from math import pi
import math

def dot(v1,v2):
    r = 0
    for i in range(len(v2)):
        r += v1[i]*v2[i];
    return r;

def vlen(v):
    r = 0
    for i in v:
        r += i*i
    return sqrt(r)


def r2d(a):
    return a * 180 / pi

def isZero(v):
    for i in range(len(v)):
        if(v[i] != 0):
            return False
        return True

def imShow(img, title="image"):
    cv2.imshow(title,img)
    cv2.waitKey(0)

def sobel(im):
    x = cv2.Sobel(im,cv2.CV_64F,1, 0, 3)
    y = cv2.Sobel(im,cv2.CV_64F,0, 1, 3)
    return (x,y)

def hist(cell):
    (dst_x,dst_y) = sobel(cell)
    sy = len(dst_y)
    sx = len(dst_y[0])
    hist = [0,0,0,0,0,0,0,0,0]
    for x in range(sx):
        for y in range(sy):
            vec = [dst_x[y][x] * 100 , dst_y[y][x] * 100]
            if(not isZero(vec)):
                e1 = [100,0]
                a = math.atan2(-vec[1] , vec[0])
                if a < 0:
						a += pi;
                a = r2d(a) % 180
                key = int(a // 20)
                hist[key] += vlen(vec)
    return hist

def maxAngle(h):
    max = 0
    for i in range(len(h)):
        if h[max] < h[i]:
            max = i
    return max * 20

def drawAngle(img, angle, minx, miny):
    angle = r2d(angle)
    x = 16
    y = 0
    xx = x * math.cos(angle) - y * math.sin(angle)
    yy = x * math.sin(angle) + y * math.cos(angle)
    xx /= vlen([xx,yy])
    yy /= vlen([xx,yy])
    xx *= 8
    yy *= 8
    xx += minx
    yy += miny
    cv2.line(img,(minx,miny), (int(xx),int(yy)),255)


def dist(a,b):
    r = 0
    for i in range(len(a)):
        r += (a[i] - b[i])**2
    return math.sqrt(r)

'''
cell
8*8 = 64
# # # # # # # #
# # # # # # # #
# # # # # # # #
# # # # # # # #
# # # # # # # #
# # # # # # # #
# # # # # # # #
# # # # # # # #

block has 4x64 = 256 = 16*16
# #
# #
'''


person = cv2.imread('person.png',0)
people = cv2.imread('people2.png',0)

print "X (width) " + str(len(person[0])) + "\nY (height) " + str(len(person))
#ymin : ymax , xmin:xmax
#imShow(img[0:100 , 10:20])

aaa  = np.zeros((len(people),len(people[0]),1), np.uint8)
# (x,y) , (x,y)
#cv2.rectangle(img, (100,0) , (200,200) , 100, 1 )

person_blocks = []

for x in range(len(person[0]) // 16 ):
    subblocks = []
    for y in range(len(person) // 16 ):
        min_x = x * 16
        max_x = (x + 1) * 16
        min_y = y * 16
        max_y = (y + 1) * 16
        block = person[min_y : max_y , min_x: max_x].copy()
        #print str(min_x) + "-" + str(max_x) + "  " + str(min_y) + "," + str(max_y)
        #cv2.rectangle(img, (min_x,min_y) , (max_x,max_y) , 100, 2)
        #cv2.imwrite(str(min_x) + "_" + str(max_x) + "foo.png",block)
        histsum = (0,0,0,0,0,0,0,0,0)
        for i in range(2):
            for k in range(2):
                min_x2 = i * 8
                max_x2 = (i + 1) * 8
                min_y2 = k * 8
                max_y2 = (k+1) * 8
                cell = block[min_y2 : max_y2 , min_x2 : max_x2].copy()
                h = hist(cell)
                histsum = [a + b for a, b in zip(histsum, h)]
                #print str(min_x2) + "-" + str(max_x2) + "  " + str(min_y2) + "  " + str(max_y2)
                #cv2.rectangle(img, (min_x2 + min_x2,min_y + min_y2) , (min_x + max_x2,min_y + max_y2) , 255, 1)
        angle = maxAngle(histsum)
        #print angle
        subblocks.append(histsum)
        #drawAngle(aaa,angle,min_x,min_y)
        #imShow(img[min_y : max_y , min_x: max_x])
    person_blocks.append(subblocks)



people_blocks = []

for x in range(len(people[0]) // 16 ):
    subblocks = []
    for y in range(len(people) // 16 ):
        min_x = x * 16
        max_x = (x + 1) * 16
        min_y = y * 16
        max_y = (y + 1) * 16
        block = people[min_y : max_y , min_x: max_x].copy()
        #print str(min_x) + "-" + str(max_x) + "  " + str(min_y) + "," + str(max_y)
        #cv2.rectangle(img, (min_x,min_y) , (max_x,max_y) , 100, 2)
        #cv2.imwrite(str(min_x) + "_" + str(max_x) + "foo.png",block)
        histsum = (0,0,0,0,0,0,0,0,0)
        for i in range(2):
            for k in range(2):
                min_x2 = i * 8
                max_x2 = (i + 1) * 8
                min_y2 = k * 8
                max_y2 = (k+1) * 8
                cell = block[min_y2 : max_y2 , min_x2 : max_x2].copy()
                h = hist(cell)
                histsum = [a + b for a, b in zip(histsum, h)]
                #print str(min_x2) + "-" + str(max_x2) + "  " + str(min_y2) + "  " + str(max_y2)
                #cv2.rectangle(img, (min_x2 + min_x2,min_y + min_y2) , (min_x + max_x2,min_y + max_y2) , 255, 1)
        angle = maxAngle(histsum)
        #print angle
        drawAngle(aaa,angle,min_x,min_y)
        subblocks.append(histsum)
        #imShow(img[min_y : max_y , min_x: max_x])
    people_blocks.append(subblocks)

print len(people_blocks)
print len(person_blocks)

minError = -1
minn = (0,0)
for row in range(len(people_blocks) - len(person_blocks)):
    for col in range(len(people_blocks[0]) - len(person_blocks[0])):
        error = 0
        for x in range(len(person_blocks)):
            for y in range(len(person_blocks[0])):
                error += dist(people_blocks[row + x][col + y], people_blocks[x][y])
        if error < minError or minError == -1:
            minError = error
            minn = (row*16,col*16)
print minn

#imShow(pople[minn[1]:(minn[1]+200) , minn[0] : (minn[0]+200)] )
cv2.rectangle(people , (minn[0] , minn[1] ), (minn[0] +  + len(person[0]) , minn[1] + len(person)) , 255 )
imShow(aaa)
#imShow(X)
#imShow(Y)


#cv2.imwrite("foo.png",cell)
