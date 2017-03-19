# CameraManager
# Singleton class for keeping an observable coordinates of a ball, found via camera input

import cv2
import threading
import random
import time


class CameraManager:

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
			self.update_observers("Location Updated:", x=self.xBallPosition, y=self.yBallPosition, updated_at=self.lastUpdated)

		print ("Ball tracking stopped.")



	def read_keyboard_input(self):
		key = raw_input('q = Exit, p = Get Ball Position \n')
		print ("Key entered: " + key)

		if key == 'q':
			self.stop_ball_tracking()

		elif key == 'p':
			print (self.get_ball_position())
			self.read_keyboard_input()

		else:
			self.read_keyboard_input()



	def get_ball_position(self):
		return [self.xBallPosition, self.yBallPosition, self.lastUpdated]



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

	def update_observers(self, *args, **keywordargs):
		for observer in self.observers:
			observer.update(*args, **keywordargs)



	def initialize_camera(self, path):
		# TODO: Might need to add code here to gracefully handle a failed camera initialization
		if path is None:
			camera = cv2.VideoCapture(0)
		else:
			camera = cv2.VideoCapture(path)




# __________________________________________________

# # USAGE
# # python ball_tracking_demo.py --video ball_tracking_example.mp4
# # python ball_tracking_demo.py

# # import the necessary packages
# from collections import deque
# import numpy as np
# # import ArgumentParser # To be removed
# import imutils

# # construct the argument parse and parse the arguments  # To be removed
# # ap = argparse.ArgumentParser()
# # ap.add_argument("-v", "--video",
# # 	help="path to the (optional) video file")
# # ap.add_argument("-b", "--buffer", type=int, default=64,
# # 	help="max buffer size")
# # args = vars(ap.parse_args())



# # define the lower and upper boundaries of the "green"
# # ball in the HSV color space, then initialize the
# # list of tracked points
# # For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
# # HSV Info: http://infohost.nmt.edu/tcc/help/pubs/colortheory/web/hsv.html
# yellowLowerThreshold = (160, 100, 140)
# yellowUpperThreshold = (179, 255, 255)
# redLowerThreshold = (0, 100, 140) 
# redUpperThreshold = (20, 255, 255) 
# pts = deque(maxlen=args["buffer"])


# # keep looping
# while True:
# 	# grab the current frame
# 	(grabbed, frame) = camera.read()

# 	# if we are viewing a video and we did not grab a frame,
# 	# then we have reached the end of the video
# 	if args.get("video") and not grabbed:
# 		break

# 	# resize the frame, blur it, and convert it to the HSV
# 	# color space
# 	frame = imutils.resize(frame, width=600)
# 	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
# 	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# 	# construct a mask for the color "orange", then perform
# 	# a series of dilations and erosions to remove any small
# 	# blobs left in the mask
# 	maskRed = cv2.inRange(hsv, redLowerThreshold, redUpperThreshold)
# 	maskYellow = cv2.inRange(hsv, yellowLowerThreshold, yellowUpperThreshold)
# 	mask = maskRed + maskYellow
# 	mask = cv2.erode(mask, None, iterations=2)
# 	mask = cv2.dilate(mask, None, iterations=2)

# 	# find contours in the mask and initialize the current
# 	# (x, y) center of the ball
# 	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
# 		cv2.CHAIN_APPROX_SIMPLE)[-2]
# 	center = None

# 	# only proceed if at least one contour was found
# 	if len(cnts) > 0:
# 		# find the largest contour in the mask, then use
# 		# it to compute the minimum enclosing circle and
# 		# centroid
# 		c = max(cnts, key=cv2.contourArea)
# 		((x, y), radius) = cv2.minEnclosingCircle(c)
# 		M = cv2.moments(c)
# 		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

# 		# only proceed if the radius meets a minimum size
# 		if radius > 1:
# 			# draw the circle and centroid on the frame,
# 			# then update the list of tracked points
# 			cv2.circle(frame, (int(x), int(y)), int(radius + 20),
# 				(0, 255, 255), 2)
# 			cv2.circle(frame, center, 5, (0, 0, 255), -1)

# 	# update the points queue
# 	pts.appendleft(center)

# 	# loop over the set of tracked points
# 	for i in xrange(1, len(pts)):
# 		# if either of the tracked points are None, ignore
# 		# them
# 		if pts[i - 1] is None or pts[i] is None:
# 			continue

# 		# otherwise, compute the thickness of the line and
# 		# draw the connecting lines
# 		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 0.5)
# 		cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0), thickness)

# 	# show the frame to our screen
# 	cv2.imshow("Frame", frame)
# 	key = cv2.waitKey(1) & 0xFF

# 	# if the 'q' key is pressed, stop the loop
# 	if key == ord("q"):
# 		break

# # cleanup the camera and close any open windows
# camera.release()
# cv2.destroyAllWindows()
