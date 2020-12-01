import numpy as np
txt = open("Missionfromserver.txt")
waypointlat = np.array([])
waypointlong = np.array([])
waypointalt = np.array([])
waypoint = False
waypointlinecounter = 0
for line in txt:
    if waypoint:
        colon = line.find(':')
        start = colon+1
        if waypointlinecounter == 0:
            lat = float(line[start:])
            waypointlat = np.append(waypointlat,lat)
        if waypointlinecounter == 1:
            long = float(line[start:])
            waypointlong = np.append(waypointlong,long)
        if waypointlinecounter == 2:
            alt = float(line[start:])
            waypointalt = np.append(waypointalt,alt)
        waypointlinecounter+=1
        if waypointlinecounter == 3:
            waypointlinecounter = 0
            waypoint = False
    if "waypoint" in line:
        waypoint = True
print(waypointlat)
print(waypointlong)
print(waypointalt)