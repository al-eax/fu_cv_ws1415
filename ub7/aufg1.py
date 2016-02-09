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
        k = pow(math.sqrt(2),i + currentOctave)
        #k = (i+1) * math.sqrt(2)
        blur = img.copy()
        cv2.GaussianBlur(src=img,dst = blur,ksize=kernelSize,sigmaX=sigma*k,sigmaY=sigma*k,borderType = cv2.BORDER_DEFAULT )
        result.append(blur)
    return result

def getDOG(gaussians):
    result = []
    for i in range(len(gaussians) -1):
        d = gaussians[i+1] - gaussians[i]
        result.append(d)
    #imShow(result[0])
    #imShow(result[len(result)-1])
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
                # 3x3x3 Cube around keypoint
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

        listOfKeypoints.append(keypoints)
    return listOfKeypoints

def draw_arrow(image, p, q, color, arrow_magnitude=9, thickness=1, line_type=8, shift=0):
    # adapted from http://mlikihazar.blogspot.com.au/2013/02/draw-arrow-opencv.html
    #SOURCE http://mlikihazar.blogspot.de/2013/02/draw-arrow-opencv.html
    # draw arrow tail
    cv2.line(image, p, q, color, thickness, line_type, shift)
    # calc angle of the arrow
    angle = np.arctan2(p[1]-q[1], p[0]-q[0])
    # starting point of first line of arrow head
    p = (int(q[0] + arrow_magnitude * np.cos(angle + np.pi/4)),
    int(q[1] + arrow_magnitude * np.sin(angle + np.pi/4)))
    # draw first half of arrow head
    cv2.line(image, p, q, color, thickness, line_type, shift)
    # starting point of second line of arrow head
    p = (int(q[0] + arrow_magnitude * np.cos(angle - np.pi/4)),
    int(q[1] + arrow_magnitude * np.sin(angle - np.pi/4)))
    # draw second half of arrow head
    cv2.line(image, p, q, color, thickness, line_type, shift)

def drawArrow(img,coords,angle,lenght):
    angle = angle * math.pi/180
    (x,y) = coords
    newCoords = (x + int(lenght * math.cos(angle)),y + int(lenght * math.sin(angle)))
    draw_arrow(img,coords,newCoords,255)
    #cv2.line(img, coords , newCoords, 255)

def drawKeypoints(IMG, keypoints,drawArrows = False):
    img = IMG.copy()
    octaves = len(keypoints)
    for i in range(octaves):
        for kp in keypoints[i]:
            ((x,y),val) = kp
            center = (x*(2**i) ,y*(2**i))
            #print center
            cv2.circle(img,center , int( 1.6* pow(math.sqrt(2),i )  ) * 5 , 255)
            if (drawArrows):
                drawArrow(img,center,val , (i+1)*10)
    return img

def deriveImg(img):
    imX = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3) #or cv2.CV_64F ?
    imY = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3) #or cv2.CV_64F ?
    #imX = cv2.filter2D(img,-1,np.array([ [1.0 , -1.0], [ 1.0 , -1.0]  ]))
    #imY = cv2.filter2D(img,-1,np.array([ [1.0, 1.0], [-1.0, -1.0]  ]))
    #imX = cv2.filter2D(img,-1,np.array([ [1.0, -1.0]  ]))
    #imY = cv2.filter2D(img,-1,np.array([ [-1.0], [1.0]  ]))
    return (imX,imY)

def dist(A,B):
    return math.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)

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

            #f(x+h) = f(x) + h*f'(x)
            #taylor
            tx = d2[y][x] + 1*dx[y][x]
            ty = d2[y][x] + 1*dy[y][x]
            #print str(d2[y][x]) + str((tx,ty))
            if (abs(d2[y][x] - tx) < 0.03 or abs(d2[y][x] - ty) < 0.03 ):
                continue


            TrH = float(dxx[y][x]) + float(dyy[y][x])
            DetH = float(dxx[y][x]) * float(dyy[y][x]) - float(dxy[y][x])**2
            if(DetH == 0):
                continue
            if( (TrH**2 / DetH) < ((r+1)**2/r) ):# < or > ?
                newDogKeypoints.append(kp)
        newKeypoints.append(newDogKeypoints)
        #print str(len(newDogKeypoints)) + " Keypoints after rejection"
        #print "---------"
    return newKeypoints

def magnitudeOrientation(L,x,y):
    (Lx,Ly) = deriveImg(L)
    m = math.sqrt( (L[y][x+1] - L[y][x-1])**2 + (L[y+1][x] - L[y-1][x]  )**2)
    #t = math.atan( (L[y+1][x] - L[y-1][x]) / (L[y][x+1] - L[y][x-1])  )
    #print t, (L[y+1][x] - L[y-1][x]) / (L[y][x+1] - L[y][x-1]) , t*180/math.pi

    #t = math.atan2( Lx[y][x] , Ly[y][x] )
    t = math.atan2(L[y+1][x] - L[y-1][x] , L[y][x+1] - L[y][x-1])
    return (m,t)

def getOridntation(L,s,_x,_y):
    #L = deriveImg(L)[1]
    hist = np.zeros(36)
    for y in range(_y - s, _y + s):
        for x in range(_x - s, _x + s):
            (m,t) = magnitudeOrientation(L,x,y)
            if (m == 0):
                continue

            #if(abs(t*180/math.pi) > 100):
            #    pass
            #print str(t) + "->" + str(t*180/math.pi)
            t *= 180/math.pi #rad to deg

            t = t % 360 #negative angles to 0-360
            #if (t > 100 and t < 230):
            #    print t


            t = t//10 #break down to 10 bins
            hist[t-1] += m
    #print hist
    (_, _, _, (_,maxAngle)) = cv2.minMaxLoc(hist)
    #print maxAngle
    return (maxAngle+1)*10

def getOrientations(keypoints,gaussians):
    newKeypoints = []
    for octave in range(len(keypoints)):
        nKps = []
        Scales = gaussians[octave]
        KPs = keypoints[octave]
        L = Scales[0]
        #imShow(L.astype(np.uint8))
        s = int((octave+1)*2.5) #windowsize for neighbors
        for kp in KPs:
            ((x,y),v) = kp
            #if neighbors are in picture
            if(y-s > 0 and x-s > 0 and y+s <len(L) and x+s <len(L[0]) ):
                ori = getOridntation(L,s,x,y)
                nKps.append(((x,y), ori ))
        newKeypoints.append(nKps)
    return newKeypoints


img = cv2.imread("Lenna.png")#cv2.imread("Lenna.png") #read image
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to gray
o1 = img.copy()
img = np.float64(img) #convert to float

(gaussians,dogs) = getDOGLaplacePyramid(img)
keypoints = getKeyPoints(dogs)

imShow(dogs[0][0], "first DOG")
imShow(dogs[3][2], "last DOG")

imShow(drawKeypoints(o1,keypoints,False), "all Keypoints")
print len(keypoints[0]) + len(keypoints[1]) + len(keypoints[2]) + len(keypoints[3])
keypoints = reject(keypoints,dogs,r=10)
imShow(drawKeypoints(o1,keypoints,False), "rejected Keypoints")
print len(keypoints[0]) + len(keypoints[1]) + len(keypoints[2]) + len(keypoints[3])
orientedKeypoints = getOrientations(keypoints,gaussians)
#o1 = drawKeypoints(o1,orientedKeypoints)
o1 = drawKeypoints(o1,orientedKeypoints, True)
imShow(o1, "detected Keypoints")

#cv2.imwrite("foo.png" , dogs[0][0].astype(np.uint8))
