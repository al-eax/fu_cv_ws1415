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
        r.append( (int(row[1]) , int(row[0])))
    return r

def imShow(img, title="image"):
    cv2.imshow(title,img)
    cv2.waitKey(0)

def points2mat(points):

    output = np.zeros((len(points),2,1),np.float32)
    for i in range(len(points)):
        output[i][0] = float(points[i][1])#
        output[i][1] = float(points[i][0])
    return output

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

corners = points2mat(readCSV())
frames = readVideoFrames()

output = np.zeros((len(frames[0][1]),len(frames[0][0]),1), np.uint8)
output[:] = 255
lk_params = dict( winSize  = (5,5),maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

frame4 = frames[0]
for i in range(len(frames) - 1):
    frame1 = frames[i]
    frame2 = frames[i+1]
    frame3 = frame1.copy()
    oldCorners = corners.copy();
    p1, st, err = cv2.calcOpticalFlowPyrLK(frame1, frame2, oldCorners, corners, **lk_params)

    for i in range(len(corners)):
        #print str(oldCorners[i]) + "  ###   " + str(oldCorners[i])
        ax = oldCorners[i][1]
        ay = oldCorners[i][0]
        bx = corners[i][1]
        by = corners[i][0]
        cv2.line(output,(ay,ax) , (by,bx) , (0),1)
        cv2.line(frame4,(ay,ax) , (by,bx) , (255),1)
        cv2.circle(frame3,(ay,ax),3,255,2)
    #imShow(frame3)



imShow(frame4,"LK")
imShow(output,"LK - BW")
