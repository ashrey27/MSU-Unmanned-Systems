from flask import Flask, jsonify, send_file
from subprocess import call
import sys
import io
import os
import shutil
import gpsd
from subprocess import Popen, PIPE
from string import Template
from struct import Struct
from threading import Thread
from time import sleep, time

import picamera
import time
from datetime import datetime
import base64


app = Flask(__name__)

camera = picamera.PiCamera()
#camera.resolution = (3280, 2464)
camera.resolution = (1024,1024)
cap_count = 0
Acap_count = 0
autopic = False
current_time = datetime.now().strftime('%Y%m%d-%H%M')
gpsd.connect()

captures_path = '/home/pi/captures/'+current_time
if not os.path.exists(captures_path):
	os.makedirs(captures_path)
	os.makedirs(captures_path+'/autopic')

@app.route('/')
def get_status():	
	return jsonify( {
		"message": "MSUUS PI PAYLOAD ONLINE"
		})

# run a command (contained in a json object) passed by POST method as a shell command on the pi
@app.route('/run_command', methods=['GET', 'POST'])
def run_command():
	request_data = request.get_json()
	subprocess.call([request_data['command'], request_data['options']])
	return Flask.jsonify( {
		"status": "ok",
		})

@app.route('/get_gps', methods=['GET'])
def get_gps():
	gpsd.get_current()
	latitude, longitude = gpsd.position()
	
	return jsonify( {
		"latitude": latitude,
		"longitude": longitude,
		})

@app.route('/take_picture', methods=['GET'])
def take_picture():
	global cap_count, camera
	cap_count += 1
	filename = captures_path+'/image_'+str(cap_count-1)+'.png'
	camera.capture(filename, format="png")

	with open(filename, "rb") as image_file:
		encoded_image = base64.b64encode(image_file.read()).decode()

	return jsonify( {
		"id": (cap_count-1),
		"filename": filename,
		"image": encoded_image,
		})

@app.route('/start_autopicture', methods=['GET'])
def start_autopicture():
	global autopic
	autopic = True
	return Flask.jsonify( {
		"message": "autopicture started",
		})

@app.route('/stop_autopicture', methods=['GET'])
def stop_autopicture():
	global autopic
	autopic = False
	return Flask.jsonify( {
		"message": "autopicture stopped",
		})


@app.route('/bottle_release')
def bottle_release():
	######################################
	#do_release():                       #
	######################################
	return jsonify( {
		"message":"bottle released",
		"release_time":time.time(),
		})

@app.route('/restart_listener')
def restart_listener():
	print('pi listener is restarting')
	'''
	executable = sys.executable
	args = sys.argv[:]
	args.insert(0, sys.executable)

	time.sleep(1)
	os.execvp(executable, args)
	'''
	subprocess.call(['python pi_listener.py'])
	time.sleep(1)
	exit()
	time.sleep(1)
	print('did it make it here?')

@app.route('/stop_listener')
def stop_listener():
	print('pi listener is stopping')
	exit()


def take_autopicture():
	global Acap_count, camera
	Acap_count += 1
	sleep(2)
	filename = captures_path+'/autopic/test_capture_'+str(cap_count-1)+'.jpg'
	camera.capture(filename)
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)


@app.route('/start_video_stream', methods=['GET', 'POST'])
def start_video_stream():
	return 0

