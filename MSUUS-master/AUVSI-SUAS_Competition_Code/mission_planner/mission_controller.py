import sys
import clr
import MissionPlanner
import MySQLdb

print 'Starting Mission Controller...\n'
clr.AddReference("MissionPlanner.Utilities")
missionData = False # is mission data available? flag
print 'Switching to Guided mode.\n'
Script.ChangeMode("Guided")                      # changes mode to "Guided"


### DB Connection ###

print 'Connecting to database...\n'
try:
	db = MySQLdb.connect(host = "localhost", user="root", passwd = "password", db ="MSUUS")
	print 'Connected.\n'
except:
	print 'Error connecting to database.\n'
	
	
### Search For Missions Loop ###

while not missionData:
	cur = db.cursor(dictionary=True) #allows execution of all SQL queries
	cur.execute("SELECT * FROM waypoints")
	if cur.fetchAll():
		missionData = True


### Download Mission Data & Set ###

for row in cur.fetchAll():
	waypoint = MissionPlanner.Utilities.Locationwp()
	MissionPlanner.Utilities.Locationwp.lat.SetValue(waypoint,row['latitude'])
	MissionPlanner.Utilities.Locationwp.lng.SetValue(waypoint,row['longitude'])
	MissionPlanner.Utilities.Locationwp.alt.SetValue(waypoint,row['altitude'])
	MAV.setGuidedModeWP(waypoint) 
	

### Reroute Around Obstacles ###
