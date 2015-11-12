import Image
import matplotlib.pyplot as plt

def rgb2hsv(rgb):
    (R,G,B) = rgb
    H = S = V = 0.0
    R = float(R / 255.0)
    G = float(G / 255.0)
    B = float(B / 255.0)

    MIN = min(R,G,B)
    MAX = max(R,G,B)


    if MIN == MAX:
        H = 0
    elif MAX == R:
        H = 60.0 * (G - B) / (MAX - MIN)
    elif MAX == G:
        H = 60.0 * (2.0 + (B - R) / (MAX - MIN))
    elif MAX == B:
        H = 60.0 * (4.0 + (R - G) / (MAX - MIN))
    if H < 0.0:
        H += 360.0

    if MAX == 0:
        S = 0
    else:
        S = (MAX - MIN)/MAX
    V = MAX
    return (H,S,V)

def getSubImg(img, x, y, width, height):
    subimg = Image.new(img.mode, (width,height))
    for i in range(width):
        for k in range(height):
            subimg.load()[i,k] = img.load()[x + i, y + k]
    return subimg

def hsvhist(img):
    resut = []
    d = {}
    i = img.load()
    #result = Image.new("RGB", img.size)
    #o = result.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            (H,S,V) = rgb2hsv(i[x,y])
            H = int(H)
            if H in d:
                d[H] += 1
            else:
                d[H] = 1
    return d

def saveHist(hist,filename):
    line = []
    maxKey = max(hist)
    minKey = min(hist)

    for i in range(minKey,maxKey + 1):
        if i in hist:
            line.append(hist[i])
        else:
            line.append(0)

    plt.ylabel("Anzahl Pixel")
    plt.xlabel("Hue")
    plt.plot(range(minKey,maxKey + 1),line)
    plt.savefig(filename)
#    plt.show()


#print rgb2hsv((72, 79, 102))
img = Image.open("racecar.png")
subimg = getSubImg(img, 460, 260, 660, 360)
subimg.save("sub.png")
hist = hsvhist(img)
subhist = hsvhist(subimg)
saveHist(hist,"hist1")
saveHist(subhist,"subhist")
