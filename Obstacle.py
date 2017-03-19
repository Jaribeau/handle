# Obstacle

import random
import threading

PLAY_FIELD_WIDTH = 2
PLAY_FIELD_LENGTH = 2
CAM_DIST_HORI = 0.5
CAM_DIST_VERT = 1.5

class Obstacle:


	def __init__(self):
		self.xPosition = 0
		self.yPosition = 0
		self.keepMoving = False

		self.speed = 0.0
		self.xSpeed = 0.0
		self.ySpeed = 0.0


		# called by GameManager
	def collides_with(self, position, radius):
		x = position[0]
		y = position[1]
		print "Obst: (", self.xPosition, ", ", self.yPosition, ")"
		print "Ball: (", x, ", ", y, ")"
		print "--"
		if (!(0 == x == PLAY_FIELD_WIDTH && 0 == y == PLAY_FIELD_LENGTH)):
			return True
		elif ((self.xPosition - radius) <= x <= (self.xPosition + radius)) and ((self.yPosition - radius) <= y <= (self.yPosition + radius)):
			return True
		else:
			return False


		# called by GameManager
	def start_movement(self):
		# Start obstacle movement thread
		self.keepMoving = True
		t1 = threading.Thread(target=self.move_obstacle)
		t1.daemon = True
		t1.start()


		# called by GameManager
	def stop_movement(self):
		self.keepMoving = False
		print ("Obstacle motion stopped.")



	# Only to be run on its own thread
	def move_obstacle(self):
		while self.keepMoving:  # Random motion until stopMovement called
			self.xPosition = random.randint(0, 10)
			self.yPosition = random.randint(0, 10)


	def set_difficulty(diff):
		if (difficulty == 0):
			speed = 0.5
			#algorithm change
		else:
			speed = 0.4
