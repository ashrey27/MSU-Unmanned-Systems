import sys, math
from math import sin, cos
#Someone is going to need to double check the math on this.
def get_location(x, y, fov, altitude, gps, heading):
	""" Takes an x,y coordinate of a target in an image, and uses the 
	current altitude, gps coordinates, and camera field of view to 
	calculate the gps position of the target. """

	# Not sure what the fov parameter is.
	# It's field of view, but what is that in code?
	dx = x*(fov[0]*altitude) # x distance from image center in meters
	dy = y*(fov[1]*altitude) # y distance from image center in meters
	
	dx = dx*cos(heading)-dy*sin(heading) # rotate x based on heading
	dy = dy*cos(heading)+dx*sin(heading) # rotate x based on heading
	
	lat = gps[0] + (180/pi)*(dy/6378137)
	lon = gps[1] + (180/pi)*(dx/6378137)/cos(gps[1])

	# Returns a 2 element list
	return [lat, lon]

	
