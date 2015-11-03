import csv
import sys
from PIL import Image

#get sub matrix from given matrix
def	getSubMat(mat,x,y,width,height):
    submat = []
    for i in range(height):
        line = []
        for k in range(width):
            line.append(mat[x + k][y + i])
        submat.append(line)
    return submat

#load csv into matrix
def csv2mat(path):
    f = open(path, 'rb')
    reader = csv.reader(f)
    mat = []
    for row in reader:
        line = []
        for col in row:
            line.append(int(col))
        mat.append(line)
    return mat

def get(mat, pixel):
    return mat[pixel[1]][pixel[0]]

#get merged color from raw bayer format
def getMergedColorFromRaw(raw, (rawx, rawy)):
    ltop = (rawx - 1, rawy +1)
    lmid = (rawx - 1, rawy)
    lbot = (rawx - 1, rawy -1)

    mtop = (rawx , rawy + 1)
    mmid = (rawx , rawy )
    mbot = (rawx , rawy -1)

    rtop = (rawx + 1, rawy + 1)
    rmid = (rawx + 1, rawy )
    rbot = (rawx + 1 ,rawy -1)

    r = g = b = 0

    if rawx % 2 == 0:
        if rawy % 2 == 0:
            '''
            G B G
            R G R
            G B G
            '''
            r = get(raw, lmid) + get(raw, rmid)
            r /= 2

            g = get(raw, ltop) + get(raw, rtop) + get(raw, lbot) + get(raw, rbot) + get(raw, mmid)
            g /= 5

            b = get(raw , mtop) + get(raw, mbot)
            b /= 2

        else:
            '''
            R G R
            G B G
            R G R
            '''
            r = get(raw, ltop) + get(raw, lbot) + get(raw,rtop) + get(raw, rbot)
            r /= 4

            g = get(raw, lmid) + get(raw, mtop) + get(raw, mbot) + get(raw, rmid)
            g /= 4

            b = get(raw, mmid)
    else:
        if rawy % 2 == 0:
            '''
            B G B
            G R G
            B G B
            '''
            r = get(raw, mmid)

            g = get(raw, lmid) + get(raw, mtop) + get(raw, mbot) + get(raw, rmid)
            g /= 4

            b = get(raw, ltop) + get(raw, lbot) + get(raw, rtop) + get(raw, rbot)
            b /= 4

        else:
            '''
            G R G
            B G B
            G R G
            '''
            r = get(raw, mtop) + get(raw, mbot)
            r /= 2

            g = get(raw, ltop) + get(raw, lbot) + get(raw, rtop) + get(raw, rbot) + get(raw,mmid)
            g /= 5

            b = get(raw, lmid) + get(raw, rmid)
            b /= 2

    return (b,g,r)

def raw2color(rawmat):
    imgSize = (len(rawmat[0]) / 3 , len(rawmat) / 3)
    img = Image.new( 'RGB',imgSize , "white")
    for x in range(imgSize[0]):
        for y in range(imgSize[1]):
            rawx = x*3 + 1
            rawy = y*3 + 1

            color = getMergedColorFromRaw(rawmat, (rawx, rawy))
            img.load()[x,y] = color
    return img

def raw2img(mat):
    imgSize = (len(mat[0]), len(mat))
    img = Image.new( 'RGB',imgSize , "black")
    for x in range(imgSize[0]):
        for y in range(imgSize[1]):
            img.load()[x,y] = mat[y][x]
    return img

raw = csv2mat("image_bayer_raw.csv")

rawimg = raw2img(raw)
rawimg.save("rawimg.png")

subraw = getSubMat(raw,350, 180, 440 - 350, 260 - 180)
subrawimg = raw2img(subraw)
subrawimg.save("subrawimg.png")

color = raw2color(raw)
color.save("colorimg.png")
