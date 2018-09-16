import requests

class UAV:

	def __init__(self, url, username, password):
		self.url = url
		self.username = username
		self.password = password
		
	def get(self, endpoint):
		r = requests.get(self.url + endpoint, auth=(self.username, self.password))
		return r.json()
		
	def bottle_drop(self):
		return self.get('/bottle_release')
		
	def take_picture(self):
		return self.get('/take_picture')
		
	def get_gpssel(self):
		return self.get('/get_gps')
		
	def start_video(self):
		return self.get('/start_video_stream')
		
	def restart(self):
		return self.get('/restart_listener')
		
	def get_info(self):
		return self.get('/')

