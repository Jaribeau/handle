# Obstacle

import random
import threading


class Obstacle:


	def __init__(self):
		self.xPosition = 0
		self.yPosition = 0
		self.keepMoving = False



	def collides_with(self, position, radius):
		x = position[0]
		y = position[1]
		if (self.xPosition - radius) <= x <= (self.xPosition + radius):	 # NOTE: Currently only checks x axis
			return True

		else:
			return False



	def start_movement(self):
		# Start obstacle movement thread
		self.keepMoving = True
		t1 = threading.Thread(target=self.move_obstacle)
		t1.daemon = True
		t1.start()



	def stop_movement(self):
		self.keepMoving = False



	# Only to be run on its own thread
	def move_obstacle(self):
		while self.keepMoving:  # Random motion until stopMovement called
			self.xPosition += random.randint(-1, 1)
			self.xPosition += random.randint(-1, 1)
