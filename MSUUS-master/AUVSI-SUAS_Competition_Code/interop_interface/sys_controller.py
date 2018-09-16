
import PIL.Image
import PIL.ImageTk
from io import BytesIO
from tkinter import *

import interop
import sys
import re
import tkinter	# is this line redundant? Since we have "from tkinter import *" above?
import UAV
import datetime
import MySQLdb
import json 
import base64



def main():


	############################################################
	########################  DEFINITONS #######################
	############################################################

	def upload_telemetry(client, last_telem, out):
		telemetry = interop.Telemetry(latitude=38.145215,
			longitude=-76.427942,
			altitude_msl=50,
			uas_heading=90)
		#send that info to the interop server
		delta = datetime.datetime.now() - last_telem
		out.set(1 / (delta.total_seconds()))
		client.post_telemetry(telemetry)

	def upload_all_targets(client, target_json, sys_db, out):		
		cur = db.cursor() #allows execution of all SQL queries
		cur.execute("SELECT * FROM targets")

		#Fetches every row of the table; 
		#Columns are as follows:
		#1st - target_id, 2 - type, 3 - latitude, 4 - longitude, 5 - orientation, 6 - shape, 7 - background-color, 8 - alphanumeric, 9 - alphanumeric_color
		# 10 - image path
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
			with open(imagedir + "/" + row[10] + '.png', 'rb') as f:
				#the 'rb' option reads the file in binary, as opposed to as a text file
				image_data = f.read()
				client.put_target_image(target.id, image_data)

	def view_current_targets(sys_db, out):
		cur = db.cursor() #allows execution of all SQL queries
		cur.execute("SELECT * FROM targets")

		for row in cur.fetchall():
			target = interop.Target(type = row[1], #indexing starts from 0, data doesn't include target_id
				latitude = row[2],
				longitude = row[3],
				orientation = row[4],
				shape = row[5],
				background_color = row[6],
				alphanumeric = row[7],
				alphanumeric_color = row[8])

			out.insert(END, target)
			out.insert(END, "\n")
			out.see(END)

	def download_mission(client, sys_db, out):
		try:
			missions = client.get_missions()
			out.insert(END, "Mission info downloaded from interoperability server\n")
			

			for wp in missions[0].mission_waypoints:
				insert_stmt = ("INSERT INTO waypoints (wp_order, latitude, longitude, altitude, type) "
	  			"VALUES (%s, %s, %s, %s, %s)")
				data = (wp.order, wp.latitude, wp.longitude, wp.altitude_msl, "waypoint")
				cur = db.cursor()
				print(insert_stmt, data)
				cur.execute(insert_stmt, data)
				db.commit()
			
			out.insert(END, "Mission info uploaded to database.\n")
			out.see(END)

		except:
			out.insert(END, 'Something went wrong when downloading mission\n')
			out.see(END)

	def download_obstacles(client, sys_db, out):
		try:
			missions = client.get_missions()
			out.insert(END, "Obstacle info downloaded from interop\n")
			

			for wp in missions[0].mission_waypoints:
				insert_stmt = ("INSERT INTO obstacles (wp_order, latitude, longitude, altitude, type) "
	  			"VALUES (%s, %s, %s, %s, %s)")
				data = (wp.order, wp.latitude, wp.longitude, wp.altitude_msl, "waypoint")
				cur = db.cursor()
				print(insert_stmt, data)
				cur.execute(insert_stmt, data)
				db.commit()
			
			out.insert(END, "Obstacle info uploaded to database.\n")
			out.insert(END, "\n")
			out.see(END)
		except:
			out.insert(END, 'Something went wrong when downloading obstacles\n')
			out.see(END)


	def bottle_drop(drone, out):
		try:
			drone.bottle_drop()
			out.insert(END, "Bottle drop signal sent\n")
			out.see(END)
		except:
			out.insert(END, "Error sending bottle drop signal\n")
			out.see(END)

	def ping_drone(drone, out):
		try:
			info = drone.get_info()
			out.insert(END, info["message"])
			out.insert(END, "\n")
			out.see(END)
		except:
			out.insert(END, "Error pinging drone.\n")
			out.see(END)

	def drone_start_video(drone, out):
		stream = drone.take_picture()
		return 0

	def drone_take_picture(drone, sys_db, out, pic_out):
		try:
			picture = drone.take_picture()
			out.insert(END, "Picture signal sent\n")
			
			insert_stmt = ("INSERT INTO target_images (id, image) VALUES (%s, %s)")
			data = (picture["id"], picture["image"])
			cur = db.cursor()
			cur.execute(insert_stmt, data)
			db.commit()
			
			im = PIL.Image.open(BytesIO(base64.b64decode(picture["image"])))
			im2 = PIL.ImageTk.PhotoImage(im.resize((180,160)).rotate(180))
			pic_out.configure(image = im2)
			pic_out.image = im2
			
			out.insert(END, "Picture: " + picture["filename"] + " uploaded to database\n")
			out.see(END)
		except:
			out.insert(END, "Error sending take picture signal\n")
			out.see(END)

	def interop_connect(url, username, password, out):
		try:
			#set up the connection to the interop server at the specified
			#url with the specified username/password
			client = interop.Client(url=url,
			                        username=username,
			                        password=password)
			out.insert(END, "Connected to " + url + " with username '" + username + "' and password '" + password + "'.\n")
			out.see(END)
		except:
			out.insert(END, "Something when wrong when trying to connect\n")	
			out.see(END)
	
	def on_closing():
		window.destroy()


	############################################################
	###################### INITIALIZATION ######################
	############################################################

	telemetry_open = False
	client = interop.Client(url='http://127.0.0.1:8000', username='testuser', password='testpass')

	datarate = 0 # to store avg datarate
	last_telem = datetime.datetime.now()

	imagedir = 'target_images'
	drone = UAV.UAV('http://192.168.1.31:5000','MSUUS','Unmanned2017')
	
	#Connect to the mySQL database
	db = MySQLdb.connect(host = "localhost", user="root", passwd = "password", db ="MSUUS")
	#Use own credentials for actual database


	############################################################
	###################### WINDOW SETUP ########################
	############################################################
	
	window = tkinter.Tk()
	
	window.protocol("WM_DELETE_WINDOW", on_closing)
	window.title("MSUUS System Software v0.6")
	window.geometry("590x560")

	url = StringVar( window )
	url.set('http://127.0.0.1:8000')
	username = StringVar( window )
	username.set('testuser')
	password = StringVar( window )
	password.set('testpass')
	

	url_label = Label( window, text="Interop URL")
	url_label.place(x=10,y=10)
	url_textbox = Entry( window, textvariable=url )
	url_textbox.place(x=100, y=10)

	username_label = Label( window, text="Username:")
	username_label.place(x=10, y=30)
	username_textbox = Entry( window, textvariable=username )
	username_textbox.place(x=100, y=30)

	password_label = Label( window, text="Password:")
	password_label.place(x=10, y=50)
	password_textbox = Entry( window, textvariable=password )
	password_textbox.place(x=100, y=50)

	output_label = Label( window, text="Output" )
	output_label.place(x=10, y=190)
	output_textbox = Text( window, width=79, wrap=WORD )
	output_textbox.place(x=10, y=210)
	output_scrollbar = Scrollbar( window, command=output_textbox.yview )
	output_textbox['yscrollcommand'] = output_scrollbar.set
	output_scrollbar.place(x=570,y=210,height=340)

	data_rate_str = StringVar( window )
	data_rate_str.set('0')
	data_rate_label = Label( window, text="Telemetry Data Rate:" )
	data_rate_label.place(x=290, y=10)
	data_rate_field = Entry( window, textvariable=data_rate_str )
	data_rate_field.place(x=430, y=10, width=60)
	
	
	last_pic = PIL.ImageTk.PhotoImage(PIL.Image.open('blank.png'))
	picture_box_label = Label( window, text="Last Image:" )
	picture_box_label.place(x=290, y=40)
	picture_box_field = Label( window, image = last_pic )
	picture_box_field.place(x=370, y=40, width = 180, height = 160)

	connect_button = Button( window, text="Interop Connect", command = lambda: interop_connect(url.get(),username.get(),password.get(),output_textbox) )
	connect_button.place(x=10, y=90)	
	
	ping_button = Button( window, text="Ping Drone", command = lambda: ping_drone(drone, output_textbox) )
	ping_button.place(x=136, y=90)
	
	take_picture_button = Button( window, text="Take Picture", command = lambda: drone_take_picture(drone, db, output_textbox, picture_box_field) )
	take_picture_button.place(x=10, y=120)
	
	auto_picture_button = Button( window, text="Auto Picture", command = lambda: drone_take_picture(drone, db, output_textbox, picture_box_field) )
	auto_picture_button.place(x=112, y=120)
	auto_picture_button.configure(state='disable')
	
	stream_button = Button( window, text="Start Stream", command = lambda: drone_start_video(drone, db, output_textbox) )
	stream_button.place(x=214, y=120)
	stream_button.configure(state='disable')
	
	target_upload_button = Button( window, text="Download Mission", command = lambda: download_mission(client, db, output_textbox) )
	target_upload_button.place(x=10, y=150)


	############################################################
	######################## MAIN LOOP #########################
	############################################################

	while True:
		upload_telemetry(client, last_telem, data_rate_str)
		last_telem = datetime.datetime.now()
		window.update_idletasks()
		window.update()
	

if __name__ == "__main__":
	main()
	db.close()
