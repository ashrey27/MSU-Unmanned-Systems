import sys
#NOTE: client.py (interop/client/interop) has the "concurrent.futures" line commented out; This is a module that comes with Python 3.3+ but not earlier; this code will work without it, but just keep it in mind.

import MySQLdb
#Used for accessing SQL databases containing the target information


#Future Improvements: make it so the user doesn't have to input so much shit.  Also include error checking so other people know what's going on.

###############################
#Uncomment below when actually testing

path = raw_input('Enter path to client interop module: ')
######################
#Path should be something like '/.../interop/client'

#Most likely the client library won't be in the same Python search path as other modules; just add the search path to the system path to make sure it can be imported, as shown below

sys.path.append(path)


import interop
import getpass #this is only for hiding the password; really not needed but I just felt like adding it.

#####################
#UNCOMMENT below when actually testing, and COMMENT OUT line 37 (example client setup)

#url_input = raw_input('Enter URL of server: ') 
#username_input = raw_input('Enter username: ')
#password_input = getpass.getpass(prompt = 'Enter password: ')
#client = interop.Client(url = url_input, username = username_input, password = password_input)
#####################

#Example:
client = interop.Client(url = 'http://localhost:8000', username = 'testuser', password = 'testpass')
#Usually the url_input is 'http://some_url:8000', username and password is whatever we're assigned, but for testing they will be 'testuser' and 'testpass' respectively

############################################
#The following code makes several assumptions (Lines 49-84):
#
# 1.  We are using the SQL database to store our target values, and we have our image files somewhere else
# 2.  The naming convention of our images puts them in the same order as our SQL db.
#      i.e. "1_red_A_red_circle.png" links this image to the first line in the SQL database.
#	Similar to the generate_image() code in target_gen.py, this tacks on a simple target id to locate it in the db.
############################################

#Locate directory containing image files
imagedir = raw_input('Input Directory storing images: ')


#Connect to the mySQL database
db = MySQLdb.connect(host = "localhost", user="root", passwd = "password", db ="MSUUS")
#Use own credentials for actual database

cur = db.cursor() #allows execution of all SQL queries
cur.execute("SELECT * FROM targets")

#Fetches every row of the table; 
#Columns are as follows:
#1st - target_id, 2 - type, 3 - latitude, 4 - longitude, 5 - orientation, 6 - shape, 7 - background-color, 8 - alphanumeric, 9 - alphanumeric_color
#note: target_id is a long/int, and latitude and longitude are floats/doubles
for row in cur.fetchall():
	target = interop.Target(type = row[1], #indexing starts from 0, data doesn't include target_id
				latitude = row[2],
				longitude = row[3],
				orientation = row[4],
				shape = row[5],
				background_color = row[6],
				alphanumeric = row[7],
				alphanumeric_color = row[8])

	target = client.post_target(target) #send target values to server
	
	#open corresponding image file.  Assumes the naming convention goes "1_lettercolor_letter_shapecolor_shape.png".  Ex. "2_white_B_green_square.png"
	with open(imagedir + "/" + str(row[0]) + '_' + row[8] + '_' + row[7] + '_' + row[6] + '_' + row[5] + '.png', 'rb') as f:
	#the 'rb' option reads the file in binary, as opposed to as a text file
		image_data = f.read()
    		client.put_target_image(target.id, image_data)

	#Example:
	#with open('/home/brian/interop/client/interop/testdata/A.jpg', 'rb') as f: 
    		

db.close()
####################################################END SQL STUFF


#This is the example JSON
#target = interop.Target(type='standard',
                        #latitude=38.145215,
                        #longitude=-76.427942,
                        #orientation='n',
                        #shape='square',
                        #background_color='green',
                        #alphanumeric='B',
                        #alphanumeric_color='white')


#login to the docker admin page to find all the new data
