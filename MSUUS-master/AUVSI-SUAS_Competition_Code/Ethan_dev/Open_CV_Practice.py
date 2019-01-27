#code mostly from https://realpython.com/python-opencv-color-spaces/
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

Cf = cv2.imread('clifford football.jpg')
Grass = cv2.imread('Grass1.png',0)
#plt.imshow(Cf)
#plt.show()
Cf_rgb = cv2.cvtColor(Cf, cv2.COLOR_BGR2RGB)
#plt.imshow(Cf_rgb)
#plt.show()
Cf_hsv = cv2.cvtColor(Cf, cv2.COLOR_BGR2HSV)
#plt.imshow(Cf_hsv)
#plt.show()
Cf_gray = cv2.cvtColor(Cf, cv2.COLOR_BGR2GRAY)
#plt.imshow(Cf_gray)
#plt.show()
"""
(thresh, im_bw) = cv2.threshold(Cf_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#plt.imshow(im_bw, cmap='Greys_r')
#plt.show()

light_red = (190, 255, 255)
dark_red = (160, 160, 150)
light_green = (100, 250, 170)
dark_green = (50, 150, 100)
light_blue = (200, 255, 100)
dark_blue = (100, 150, 40)
#lo_square = np.full((10, 10, 3), light_green, dtype=np.uint8) / 255.0
#do_square = np.full((10, 10, 3), dark_green, dtype=np.uint8) / 255.0
#plt.subplot(1, 2, 1)
#plt.imshow(hsv_to_rgb(do_square))
#plt.subplot(1, 2, 2)
#plt.imshow(hsv_to_rgb(lo_square))
#plt.show()
mask = cv2.inRange(Cf_hsv, dark_red, light_red)
result = cv2.bitwise_and(Cf_rgb, Cf_rgb, mask=mask)
plt.subplot(1, 2, 1)
plt.imshow(mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()
"""
"""
# Read image
im = cv2.imread("clifford football.jpg", cv2.IMREAD_GRAYSCALE)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 950

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.01

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
"""
#img = cv2.imread('image0 copy.jpg')
#img = cv2.imread('smiley_grass_black.jpg')
#img = cv2.imread('smiley_grass_white.jpg')
#img = cv2.imread('Grass_pentagon.jpg')
#img = cv2.imread('smiley_grass.jpg')
#img = cv2.imread('Grass_big_pentagon.jpg')
#img = cv2.imread('Grass_pentagon.jpg')
img = cv2.imread('InkedGrass1.jpg')
#img = cv2.imread('test copy.jpeg')
#img = cv2.imread('test_image copy.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
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
img[markers == -1] = [255, 0, 0]
loc = []
for i in range(len(markers)):
    for j in range(len(markers[i])):
        if markers[i][j] == 1:
            loc.append((i, j))
#loc = np.array([[(markers[i] != 0) for i in range(len(markers[j]))] for j in range(len(markers))])
print(loc)
print(len(loc))
loc.pop(0)
x = []
for i in range(len(loc)):
    x.append(loc[i][0])
print(x)
y = []
for i in range(len(loc)):
    y.append(loc[i][1])
print(y)
minx = np.min(x)
miny = np.min(y)
maxx = np.max(x)
maxy = np.max(y)
print(minx)
print(miny)
print(maxx)
print(maxy)
 #color of markers
#print(img[markers==-1])
plt.imshow(img)
plt.show()
roi = gray[minx:maxx, miny:maxy]
roi_rgb = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB)
plt.imshow(roi_rgb)
plt.show()

