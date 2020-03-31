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
img = cv2.imread('DSC00342.JPG')
#img = cv2.imread('DSC00343.JPG')
#img = cv2.imread('DSC00344.JPG')
#img = cv2.imread('DSC00345.JPG')
#img = cv2.imread('DSC00346.JPG')
#img = cv2.imread('DSC00347.JPG')
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
    plt.imshow(hsv)
    plt.show()
    mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 190))
    ## slice the brown and dull
    imask = mask <= 0
    brown = np.zeros_like(hsv, np.uint8)
    brown[imask] = hsv[imask]
    plt.imshow(brown)
    plt.show()

    img = cv2.cvtColor(brown, cv2.COLOR_HSV2RGB)

    # from https://stackoverflow.com/questions/37803903/opencv-and-python-for-auto-cropping
    imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgray = cv2.blur(imgray, (15, 15))
    ret, thresh = cv2.threshold(imgray, math.floor(np.average(imgray)), 255, cv2.THRESH_BINARY_INV)
    dilated = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)))
    _, contours, _ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

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
    plt.imshow(out)
    plt.show()


crop_img(img,0)
roi = cv2.imread("roi.jpg",cv2.COLOR_BGR2RGB)

#color identification:

red = roi[:,:,2]
red_color_x = []
red_color_y = []
for i in range(red[0]):
    for k in i:
        if i[k] > 0:
            red_color_x.append(i)
            red_color_y.append(i)
print(red_color_x)
print(red_color_y)
plt.imshow(red)
plt.show()

#shape detection

gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)


ret,thresh = cv2.threshold(gray,127,255,1)

print(len(cv2.findContours(thresh,1,2)))
contours = cv2.findContours(thresh,1,2)
#print(contours)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print(approx)
    if len(approx)==5:
        print("pentagon")
        cv2.drawContours(roi,[cnt],0,255,-1)
    elif len(approx)==3:
        print("triangle")
        cv2.drawContours(roi,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
        print("square")
        #cv2.drawContours(roi_rgb,[cnt],0,(0,0,255),-1)
    elif len(approx) == 9:
        print("half-circle")
        cv2.drawContours(roi,[cnt],0,(255,255,0),-1)
    elif len(approx) > 15:
        print("circle")
        cv2.drawContours(roi,[cnt],0,(0,255,255),-1)
plt.subplot(1, 2, 1)
plt.imshow(roi)
plt.subplot(1, 2, 2)
roi_rgb = roi[60:80,70:90]
plt.imshow(roi_rgb)
plt.show()
