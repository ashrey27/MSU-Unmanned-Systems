import interop
import sys
import re
import Tkinter
from Tkinter import *


def main():

	############################################################
	###################### INITIALIZATION ######################
	############################################################

	telemetry_open = False
	client = interop.Client(url='http://127.0.0.1:8000', username='testuser', password='testpass')
	sys_db = database.db_connectt(url='http://127.0.0.1:8000', username='testuser', password='testpass')
	drone = UAV.connect(url='http://127.0.0.1:8000', username='testuser', password='testpass')
	dataRate = 0

	############################################################
	###################### API DEFINITONS ######################
	############################################################

	def upload_telemetry(client, out):
                telemetry = interop.Telemetry(latitude=38.145215,
			longitude=-76.427942,
			altitude_msl=50,
			uas_heading=90)
                #send that info to the interop server
                client.post_telemetry(telemetry)
		out.insert(END,"Telemetry posted\n")

	def upload_all_targets(client, target_json, sys_db, out):
		# this is all boilerplate right now, we need to send target info as json
		# or extract the json info and send it this way.
		try:
                        #create a target object. we will be building this object
                        #the output of our image classification program, from v$
                        #stored in our database.
                        targets, confidence = sys_db.get_all_targets()
			target_count = 0
			confirmed_targets = []
			for i in range(0,len(targets)):
				if confidence[i] > 90:
					confirmed_targets.append(targets[i])


                        #send the target info to the interop server
			for i in range(0,confirmed_targets):
                        	client.post_target(confirmed_targets[i])
		except:
			out.insert(END, 'Something went wrong when uploading target\n')

	def view_current_targets(sys_db, out):
		#do that

	def upload_mission(client, mission_json, sys_db, out):
		# this is all boilerplate right now, we need to send mission info as json
		# or extract the json info and send it this way.
		try:
                        mission = sys_db.get_mission()
                        #send the mission info to the interop server
                        mission = client.post_target(mission)
                        out.insert(END, "Mission posted\n")
		except:
			out.insert(END, 'Something went wrong when uploading mission\n')

	def view_mission(sys_db, out):
		#do that

	def bottle_drop(drone, out):
		try:
			drone.bottle_drop()
                	out.insert(END, "Bottle drop signal sent\n")
		except:
                        out.insert(END, "Error sending bottle drop signal\n")

	def get_drone_info(drone, out):
		#do that

	def drone_start_video(drone, out):
		#do that

	def drone_take_picture(drone, out):
		#do that

	def connect(url, username, password, out):
		try:
			#set up the connection to the interop server at the specified
			#url with the specified username/password
			client = interop.Client(url=url,
			                        username=username,
			                        password=password)
			out.insert(END, "Connected to " + url + " with username '" + username + "' and password '" + password + "'.\n")
		except:
			out.insert(END, "Something when wrong when trying to connect\n")
	

	############################################################
	###################### WINDOW SETUP ########################
	############################################################

	window = Tkinter.Tk()
	window.title("MSUUS")
	window.geometry("590x560")

        url = StringVar( window )
        url.set('http://127.0.0.1:8000')
        username = StringVar( window )
        username.set('testuser')
        password = StringVar( window )
        password.set('testpass')
	
	url_label = Label( window, text="Server URL")
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
	
	data_rate_label = Label( window, text="Telemetry Data Rate:" )
	data_rate_label.place(x=290, y=10)
	data_rate_field = Entry( window, textvariable=dataRate )
	data_rate_field.place(x=430, y=10, width=40)

	connect_button = Button( window, text="Connect", command = lambda: connect(url.get(),username.get(),password.get(),output_textbox) )
	connect_button.place(x=10, y=90)

	target_upload_button = Button( window, text="Upload Target", command = lambda: upload_target(client, "{'id':1}",output_textbox) )
	target_upload_button.place(x=10, y=150)
	

	window.after(500, lambda: upload_telemetry(client,output_textbox))	
	window.mainloop()


if __name__ == "__main__":
	main()
