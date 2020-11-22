#code mostly from https://realpython.com/python-opencv-color-spaces/
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import math
#test images
#img = cv2.imread('image0 copy.jpg')
#img = cv2.imread('smiley_grass_black.jpg')
#img = cv2.imread('smiley_grass_white.jpg')
#img = cv2.imread('smiley_grass.jpg')
#img = cv2.imread('Grass_big_pentagon.jpg')
#img = cv2.imread('Grass_pentagon.jpg')
#img = cv2.imread('Grass1_2_red_square.jpg')
#img = cv2.imread('InkedGrass1.jpg')
#img = cv2.imread('test copy.jpeg')
#img = cv2.imread('test_image copy.png')
#img = cv2.imread('Grass_tiles.PNG')
#img = cv2.imread('DSC00342.JPG') # blue w/ yellow letter
#img = cv2.imread('DSC00343.JPG') # yellow w/ black letter
#img = cv2.imread('DSC00344.JPG') # blue w/ yellow letter
#img = cv2.imread('DSC00345.JPG') # blue w/ black letter
img = cv2.imread('DSC00346.JPG') # lavendar w/ orange letter
#img = cv2.imread('DSC00347.JPG') # red w/ black letter
#img = cv2.imread('DSC00348.JPG')
#img = cv2.imread('DSC00349.JPG')
#img = cv2.imread('DSC00350.JPG')
#img = cv2.imread('DSC00351.JPG')
#img = cv2.imread('597.jpg')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

def crop_img(img,indx,done=False):
    plt.imshow(img)
    plt.show()
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    #plt.imshow(hsv)
    #plt.show()
    mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 190))
    ## slice the brown and dull
    imask = mask <= 0
    brown = np.zeros_like(hsv, np.uint8)
    brown[imask] = hsv[imask]
    #plt.imshow(brown)
    #plt.show()

    mask = cv2.inRange(brown, (0, 0, 190), (100, 80, 255))
    ## slice the white
    imask = mask <= 0
    white = np.zeros_like(brown, np.uint8)
    white[imask] = brown[imask]
    #plt.imshow(white)
    #plt.show()

    img = cv2.cvtColor(white, cv2.COLOR_HSV2RGB)

    # from https://stackoverflow.com/questions/37803903/opencv-and-python-for-auto-cropping
    imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgray = cv2.blur(imgray, (15, 15))
    ret, thresh = cv2.threshold(imgray, math.floor(np.average(imgray)), 255, cv2.THRESH_BINARY_INV)
    dilated = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)))
    contours, _ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    new_contours = []
    for c in contours:
        # if cv2.contourArea(c) < 960000:
        if 100000 < cv2.contourArea(c) < 20000000:
            new_contours.append(c)

    best_box = [-1, -1, -1, -1]
    for c in new_contours:
        x, y, w, h = cv2.boundingRect(c)
        if best_box[0] < 0:
            best_box = [x, y, x + w, y + h]
        else:
            if x < best_box[0]:
                best_box[0] = x - 5
            if y < best_box[1]:
                best_box[1] = y - 5
            if x + w > best_box[2]:
                best_box[2] = x + w + 5
            if y + h > best_box[3]:
                best_box[3] = y + h + 5

    out = img[best_box[1]:best_box[3], best_box[0]:best_box[2]]
    #plt.imshow(out)
    #plt.show()
    return out


roi = crop_img(img,0)
#roi = cv2.imread("roi.jpg",cv2.COLOR_BGR2RGB)
plt.imshow(roi)
plt.show()


#color identification:

pixels = []
for i in range(1, int(len(roi) / 5)):
    for k in range(1, int(len(roi[5*i]) / 5)):
        #print(roi[5*i, k, 0])
        if roi[5*i, 5*k, 0] != 0 or roi[5*i, 5*k, 1] != 0 or roi[5*i, 5*k, 2] != 0:
            pixels.append(list(roi[5*i, 5*k]))
#print(pixels)

sumr = 0
for i in pixels:
    sumr += i[0]
averager = sumr / len(pixels)
print("red average = ", averager)
sumg = 0
for j in pixels:
    sumg += j[1]
averageg = sumg / len(pixels)
print("green average = ", averageg)
sumb = 0
for k in pixels:
    sumb += k[2]
averageb = sumb / len(pixels)
print("blue average = ", averageb)

letterPixels = []
for i in pixels:
    if (i[0] > averager + 20 or i[0] < averager - 20) and (i[1] > averageg + 20 or i[1] < averageg - 20) and (i[2] > averageb + 20 or i[2] < averageb - 20):
        letterPixels.append(i)
#print(letterPixels)

letterSumr = 0
for i in letterPixels:
    letterSumr += i[0]
letterAverager = letterSumr / len(letterPixels)
print("red letter average = ", letterAverager)
letterSumg = 0
for i in letterPixels:
    letterSumg += i[1]
letterAverageg = letterSumg / len(letterPixels)
print("green letter average = ", letterAverageg)
letterSumb = 0
for i in letterPixels:
    letterSumb += i[2]
letterAverageb = letterSumb / len(letterPixels)
print("blue letter average = ", letterAverageb)

#highest r w/ low g&b
redupper = [255, 120, 120]
redlower = [75, 0, 0]

#highest r w/ high g & low b
orangeupper = [255, 200, 95]
orangelower = [170, 110, 0]

#highest r w/ almost equal g
yellowupper = [255, 255, 155]
yellowlower = [210, 208, 0]

#highest g w/ higher r & middle b
greenupper = [175, 255, 150]
greenlower = [15, 60, 0]

#highest b w/ almost equal g
cyanupper = [175, 250, 255]
cyanlower = [0, 75, 80]

#highest b w/ low r and g
blueupper = [55, 55, 255]
bluelower = [0, 0, 205]

#highest b w/ high r
purpleupper =[210, 175, 255]
purplelower = [25, 0, 60]

#highest r w/ almost equal b
pinkupper = [255, 200, 255]
pinklower = [210, 0, 200]

#shape color
if (averager <= redupper[0] and averager >= redlower[0]) and (averageg <= redupper[1] and averageg >= redlower[1]) and (averageb <= redupper[2] and averageb >= redlower[2]):
    print("Shape is red")
elif (averager < orangeupper[0] and averager > orangelower[0]) and (averageg < orangeupper[1] and averageg > orangelower[1]) and (averageb < orangeupper[2] and averageb > orangelower[2]):
    print("Shape is orange")
elif (averager < yellowupper[0] and averager > yellowlower[0]) and (averageg < yellowupper[1] and averageg > yellowlower[1]) and (averageb < yellowupper[2] and averageb > yellowlower[2]):
    print("Shape is yellow")
elif (averager < greenupper[0] and averager > greenlower[0]) and (averageg < greenupper[1] and averageg > greenlower[1]) and (averageb < greenupper[2] and averageb > greenlower[2]):
    print("Shape is green")
elif (averager < cyanupper[0] and averager > cyanlower[0]) and (averageg < cyanupper[1] and averageg > cyanlower[1]) and (averageb < cyanupper[2] and averageb > cyanlower[2]):
    print("Shape is cyan")
elif (averager < blueupper[0] and averager > bluelower[0]) and (averageg < blueupper[1] and averageg > bluelower[1]) and (averageb < blueupper[2] and averageb > bluelower[2]):
    print("Shape is blue")
elif (averager < purpleupper[0] and averager > purplelower[0]) and (averageg < purpleupper[1] and averageg > purplelower[1]) and (averageb < purpleupper[2] and averageb > purplelower[2]):
    print("Shape is purple")
elif (averager < pinkupper[0] and averager > pinklower[0]) and (averageg < pinkupper[1] and averageg > pinklower[1]) and (averageb < pinkupper[2] and averageb > pinklower[2]):
    print("Shape is pink")
else:
    print("Shape is black")

#letter color
if (letterAverager <= redupper[0] and letterAverager >= redlower[0]) and (letterAverageg <= redupper[1] and letterAverageg >= redlower[1]) and (letterAverageb <= redupper[2] and letterAverageb >= redlower[2]):
    print("Letter is red")
elif (letterAverager < orangeupper[0] and letterAverager > orangelower[0]) and (letterAverageg < orangeupper[1] and letterAverageg > orangelower[1]) and (letterAverageb < orangeupper[2] and letterAverageb > orangelower[2]):
    print("Letter is orange")
elif (letterAverager < yellowupper[0] and letterAverager > yellowlower[0]) and (letterAverageg < yellowupper[1] and letterAverageg > yellowlower[1]) and (letterAverageb < yellowupper[2] and letterAverageb > yellowlower[2]):
    print("Letter is yellow")
elif (letterAverager < greenupper[0] and letterAverager > greenlower[0]) and (letterAverageg < greenupper[1] and letterAverageg > greenlower[1]) and (letterAverageb < greenupper[2] and letterAverageb > greenlower[2]):
    print("Letter is green")
elif (letterAverager < cyanupper[0] and letterAverager > cyanlower[0]) and (letterAverageg < cyanupper[1] and letterAverageg > cyanlower[1]) and (letterAverageb < cyanupper[2] and letterAverageb > cyanlower[2]):
    print("Letter is cyan")
elif (letterAverager < blueupper[0] and letterAverager > bluelower[0]) and (letterAverageg < blueupper[1] and letterAverageg > bluelower[1]) and (letterAverageb < blueupper[2] and letterAverageb > bluelower[2]):
    print("Letter is blue")
elif (letterAverager < purpleupper[0] and letterAverager > purplelower[0]) and (letterAverageg < purpleupper[1] and letterAverageg > purplelower[1]) and (letterAverageb < purpleupper[2] and letterAverageb > purplelower[2]):
    print("Letter is purple")
elif (letterAverager < pinkupper[0] and letterAverager > pinklower[0]) and (letterAverageg < pinkupper[1] and letterAverageg > pinklower[1]) and (letterAverageb < pinkupper[2] and letterAverageb > pinklower[2]):
    print("Letter is pink")
else:
    print("Letter is black")


#shape detection

#gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)


#ret,thresh = cv2.threshold(gray,127,255,1)

#print(len(cv2.findContours(thresh,1,2)))
#contours = cv2.findContours(thresh,1,2)
#print(contours)

#for cnt in contours:
#    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
#    print(approx)
#    if len(approx)==5:
#        print("pentagon")
#        cv2.drawContours(roi,[cnt],0,255,-1)
#    elif len(approx)==3:
#        print("triangle")
#        cv2.drawContours(roi,[cnt],0,(0,255,0),-1)
#    elif len(approx)==4:
#        print("square")
        #cv2.drawContours(roi_rgb,[cnt],0,(0,0,255),-1)
#    elif len(approx) == 9:
#        print("half-circle")
#        cv2.drawContours(roi,[cnt],0,(255,255,0),-1)
#    elif len(approx) > 15:
#        print("circle")
#        cv2.drawContours(roi,[cnt],0,(0,255,255),-1)
#plt.subplot(1, 2, 1)
#plt.imshow(roi)
#plt.subplot(1, 2, 2)
#roi_rgb = roi[60:80,70:90]
#plt.imshow(roi_rgb)
#plt.show()
