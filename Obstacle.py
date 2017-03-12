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
		print "Obst: (", self.xPosition, ", ", self.yPosition, ")"
		print "Ball: (", x, ", ", y, ")"
		print "--"
		if ((self.xPosition - radius) <= x <= (self.xPosition + radius)) and ((self.yPosition - radius) <= y <= (self.yPosition + radius)):
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
		print "Obstacle motion stopped."



	# Only to be run on its own thread
	def move_obstacle(self):
		while self.keepMoving:  # Random motion until stopMovement called
			self.xPosition = random.randint(0, 10)
			self.yPosition = random.randint(0, 10)
