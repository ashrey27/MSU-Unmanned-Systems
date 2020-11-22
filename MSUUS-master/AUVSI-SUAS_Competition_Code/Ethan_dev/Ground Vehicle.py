import numpy as np
import math

def angle_sub(ang1,ang2):
    if ang1 < 0:
        ang1 = 2*np.pi+ang1
    if ang2 < 0:
        ang2 = 2*np.pi+ang2
    angdiff = ang1-ang2
    return angdiff

def PID(K,gps,goal):
    thetagoal = math.atan2(goal.y-gps.y,goal.x-gps.x)
    while True:
        w=K*angle_sub(thetagoal,gps.ang) #rotational velocity
        v = K*np.sqrt((goal.y-gps.y)**2+(goal.x-gps.x)**2) #linear velocity
        if gps == goal:
            break

