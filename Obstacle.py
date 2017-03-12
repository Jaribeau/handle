# Obstacle

import random
import threading

class Obstacle:


	def __init__(self):
		self.xPosition = 0
		self.yPosition = 0
		self.keepMoving = False



	def collidesWith(self, position, radius):
		x = position[0]
		y = position[1]
		if x >= (self.xPosition - radius) and x <= (self.xPosition + radius):	# NOTE: Currently only checks x axis
			return True

		else:
			return False



	def startMovement(self):
		# Start obstacle movement thread
		self.keepMoving = True
		t1 = threading.Thread(target = self.moveObstacle)
		t1.daemon = True
		t1.start()



	def stopMovement(self):
		self.keepMoving = False



	# Only to be run on its own thread
	def moveObstacle(self):
		while self.keepMoving == True:	# Random motion until stopMovement called
			self.xPosition += random.randint(-1, 1)
			self.xPosition += random.randint(-1, 1)
