#code mostly from https://realpython.com/python-opencv-color-spaces/
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
#test images
#img = cv2.imread('image0 copy.jpg')
#img = cv2.imread('smiley_grass_black.jpg')
#img = cv2.imread('smiley_grass_white.jpg')
#img = cv2.imread('smiley_grass.jpg')
#img = cv2.imread('Grass_big_pentagon.jpg')
img = cv2.imread('Grass_pentagon.jpg')
#img = cv2.imread('Grass1_2_red_square.jpg')
#img = cv2.imread('InkedGrass1.jpg')
#img = cv2.imread('test copy.jpeg')
#img = cv2.imread('test_image copy.png')
#img = cv2.imread('Grass_tiles.PNG')
#img = cv2.imread('DSC00342.JPG')
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

    if done is False:
        plt.imshow(img)
        plt.show()
        #sets the background of the image to black
        mask = np.zeros(img.shape[:2],np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        rect = (50,50,450,290)
        cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img = img*mask2[:,:,np.newaxis]
        plt.imshow(img)
        #plt.show()

    #picks out a specific object in the image and crops out everything but that
    #code from opencv's website on watershed
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [255, 255, 255]
    loc = []
    plt.imshow(img)
    plt.show()

    #performs the cropping of the image
    for i in range(len(markers)):
        for j in range(len(markers[i])):
            if markers[i][j] == 1:
                loc.append((i, j))
    if len(loc) > 1:
        loc.pop(0)
        x = []
        for i in range(len(loc)):
            x.append(loc[i][0])
        y = []
        for i in range(len(loc)):
            y.append(loc[i][1])
        minx = np.min(x)-3
        miny = np.min(y)-3
        maxx = np.max(x)+3
        maxy = np.max(y)+3
        img[markers == -1] = [255, 0, 0]
        plt.imshow(img)
        plt.show()
        roi = img[minx:maxx, miny:maxy]
        #roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        plt.imshow(roi)
        plt.show()
        cv2.imwrite("roi.jpg",roi)
"""
    #splits image to look for more objects
    i = 0
    j = 0
    x = x-minx
    y = y-miny
    xmin2 = np.min(x)
    ymin2 = np.min(y)
    xmax2 = xmin2
    ymax2 = ymin2
    while (x[i]-x[i+1]) < 4 and i < len(x)-2:
        xmax2 = x[i]
        i += 1
    xmin2 = minx

    while (y[j]-y[j+1]) < 4 and j < len(y)-2:
        ymax2 = y[j]
        j += 1
    ymin2 = miny
    print(y[j])
    print(x[i])
    print(xmin2)
    print(xmax2)
    print(ymin2)
    print(ymax2)
    img1 = roi[minx:xmax2, miny:ymax2]
    cv2.imwrite("output1.jpg",img1)
    plt.imshow(img1)
    plt.show()
    k = xmin2
    l = ymin2
    #print(len(roi_rgb[0][:]))
    #print(len(roi_rgb[:][0]))
    while k < xmax2:
        while l < ymax2:
            #print(k,l)
            roi[k,l] = [0,0,0]
            l += 1
        l = ymin2
        k += 1
    crop_img(roi,0,True)
    """


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
