# BallTracker
# Singleton class for keeping an observable coordinates of a ball, found via camera input

import cv2
import threading
import random
import time


class BallTracker:

	# Make this private
	def __init__(self):
		self.ballTrackingEnabled = False
		self.xBallPosition = 0
		self.yBallPosition = 0
		self.lastUpdated = time.localtime()
		self.ballRadius = 3  # NOTE: This is a magic number and should be moved to a "physical properties" class
		self.observers = []


	# TODO: Make singleton
	# def getInstance(self):



	def start_ball_tracking(self):
		# TODO: Handle case where already started

		self.ballTrackingEnabled = True

		# Start ball tracking thread
		t1 = threading.Thread(target=self.track_ball)
		t1.daemon = True
		t1.start()

		# Listen for keyboard input to manually trigger ball tracking commands
		# t2 = threading.Thread(target = self.readKeyboardInput())
		# t2.daemon = True
		# t2.start()



	def stop_ball_tracking(self):
		self.ballTrackingEnabled = False



	# Only to be run on its own thread
	def track_ball(self):
		while self.ballTrackingEnabled:
			self.xBallPosition = random.randint(0, 10)  # temp placeholder for vision tracking results
			self.yBallPosition = random.randint(0, 10)  # temp placeholder for vision tracking results
			self.lastUpdated = time.clock()
			self.push_notification("Location Updated:", x=self.xBallPosition, y=self.yBallPosition, updated_at=self.lastUpdated)

		print "Ball tracking stopped."



	def read_keyboard_input(self):
		key = raw_input('q = Exit, p = Get Ball Position \n')
		print "Key entered: " + key

		if key == 'q':
			self.stop_ball_tracking()

		elif key == 'p':
			print self.get_ball_position()
			self.read_keyboard_input()

		else:
			self.read_keyboard_input()



	# def get_ball_position(self):
	# 	return [self.xBallPosition, self.yBallPosition, self.lastUpdated]



	def get_ball_radius(self):
		return self.ballRadius



	# Observer Functions
	def register(self, observer):
		if observer not in self.observers:
			self.observers.append(observer)

	def unregister(self, observer):
		if observer in self.observers:
			self.observers.remove(observer)

	def unregister_all(self):
		if self.observers:
			del self.observers[:]

	def push_notification(self, *args, **keywordargs):
		for observer in self.observers:
			observer.notify(*args, **keywordargs)



	def initialize_camera(self, path):
		# TODO: Might need to add code here to gracefully handle a failed camera initialization
		if path is None:
			camera = cv2.VideoCapture(0)
		else:
			camera = cv2.VideoCapture(path)


