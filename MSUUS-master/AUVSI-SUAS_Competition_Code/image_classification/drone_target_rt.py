# This code looks like it might have been used to interpret a video stream?
# Not sure when that was ever a possibility.
# Looking like a frame grabber from video then 
# to some pre-processing?
# Can't really tell what happens after that.
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

camera = cv2.VideoCapture(args["Video"])

while True:
	(grabbed, frame) = camera.read()
	status = "No Targets"

	if not grabbed:
		break

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (7, 7), 0)
	edged = cv2.Canny(blurred, 50, 150)

	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
