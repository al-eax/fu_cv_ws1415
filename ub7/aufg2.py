import csv
import sys
import numpy as np
import cv2
import cv
import math

def imShow(img, title="image"):
    cv2.imshow(title,img)
    cv2.waitKey(0)

def readCSV(path):
    r = []
    f = open(path, 'rb')
    reader = csv.reader(f)
    for row in reader:
        r.append(row)
    return r

def dist(A,B):
    s = 0
    for i in range(len(A)):
        s += (float(A[i]) - float(B[i]))**2
    return math.sqrt(s)

def nearstNaighbor(A, Bs):
    d = dist(A,Bs[0])
    index = 0
    for i in range(len(Bs)):
        B = Bs[i]
        tmp = dist(A,B)
        if tmp < d:
            index = i
            d = tmp
    return (index, d)

def match(As,Bs):
    result = []
    for a in range(len(As)):
        (b,d ) = nearstNaighbor(As[a],Bs)
        result.append( [d,a,b] )
    return result

def drawKeypoints(img1,img2,locsA,locsB ,matches):
    (width,height) = (len(img1[0]) + len(img2[0]), max(len(img1), len(img2)))
    newImg = np.zeros((height,width)).astype(np.uint8)

    for y in range(len(img1)):
        for x in range(len(img1[0])):
            newImg[y][x] = img1[y][x]

    for y in range(len(img2)):
        for x in range(len(img2[0])):
            #print  img2[y][x]
            newImg[y][x + len(img1[0])] = img2[y][x]
    #imShow(newImg)
    for lst in matches:
        D = lst[0]
        ia = lst[1]
        ib = lst[2]
        A = locsA[ia]
        B = locsB[ib]
        pA =  (int(float(A[1])),int(float(A[0])))
        pB = (len(img2[0]) + int(float(B[1])) , int(float(B[0])))
        cv2.line(newImg ,pA   , pB , 255 )
    imShow(newImg)

def filter(matches):
    return sorted(matches, key=lambda x : x[0])

l_locs = readCSV("locs_Lenna.csv")
l_desc = readCSV("desc_Lenna.csv")

lt_locs = readCSV("locs_Lenna_transformed.csv")
lt_desc = readCSV("desc_Lenna_transformed.csv")

img1 = cv2.imread("Lenna.png",0)
img2 = cv2.imread("Lenna_transformed.png",0)

matches = match(l_desc[0:100],lt_desc[0:100])
matches = filter(matches)[0:40]
drawKeypoints(img1,img2,l_locs,lt_locs,matches)
