import csv
import sys
import numpy as np
import cv2
import cv

def readCSV(path = "corners.cvs"):
    r = []
    f = open(path, 'rb')
    reader = csv.reader(f)
    for row in reader:
        r.append( (int(row[0]) , int(row[1])))
    return r

def imShow(img, title="image"):
    cv2.imshow(title,img)
    cv2.waitKey(0)

def readVideoFrames(path = "beedance.avi", frames = -1):
    cap = cv2.VideoCapture(path)
    result = []
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if(ret == False):
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result.append(frame)
        i +=1
        if (i == frames):
            break
    cap.release()
    return result

def sobel(img):
    x= cv2.Sobel(img,cv2.CV_8UC1,1, 0, 3)
    y= cv2.Sobel(img,cv2.CV_8UC1,0, 1, 3)
    return (x,y)

def getH(frame1, frame2, point):
    (px,py) = point
    F = frame1[ py - 3 : py + 2 , px - 3 : px + 2] #
    G = frame2[ py - 3 : py + 2 , px - 3 : px + 2]
    (FDx,FDy) = sobel(F)
    FDsum = (0,0) # x,y
    Dot = 0
    if(len(F) == 0):
        return (0,0)
    for x in range(len(F[0])):
        for y in range(len(F)):
            fdx = int(FDx[y,x])# F'(x)
            fdy = int(FDy[y,x])# F'(x)
            v = int(G[y,x]) - int(F[y,x]) # F(x) - G(x)
            FDsum = (FDsum[0] +  fdx * v ,FDsum[1] +  fdy * v ) #Sum[ F'(x) * G(x) - F(x) ]
            Dot += (fdx * fdx) + (fdy * fdy) #Sum[F'(x) * F'(x)]
    if(Dot == 0):
        return (0,0)
    h = (float(FDsum[0]) / float(Dot) , float(FDsum[1]) / float(Dot) )
    print h
    #fx = F[py,px] + (h[0]*FDx[1] + h[1] * FDx[0])
    return  h


corners = readCSV()
frames = readVideoFrames()#(frames = 10)

output = np.zeros((len(frames[0][1]),len(frames[0][0]),1), np.uint8)
for i in range(len(frames) -1):
    frame1 = frames[i]
    frame2 = frames[i+1]
    for c in range(len(corners)):
        corner = corners[c]
        h = getH(frame1, frame2, corner) #x,y
        predicted = (int(corner[0] + h[1]),int(corner[1] + h[0])) #y,x
        #print str(corner) + " - " + str(predicted) + " - " + str(h)
        cv2.line(output, corner, predicted, (255), 1)
        corners[c] = predicted
imShow(output)
