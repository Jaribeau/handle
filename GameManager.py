# GameManager

from CameraManager import CameraManager
from Obstacle import Obstacle


class GameManager:


	def __init__(self):
		self.cameraManager = CameraManager()
		self.obstacle = Obstacle()
		self.timeRemaining = 60000
		self.gameOn = False



	def start_game(self):
		self.cameraManager.start_ball_tracking()
		self.obstacle.start_movement()
		self.timeRemaining = 60000
		self.gameOn = True


		print "Starting Game!!!"
		print "----------------"

		while self.gameOn:

			if self.is_collision(self.cameraManager, self.obstacle):
				print "------- Collision!!! --------"
				self.gameOn = False

			else:
				print "."

		print "Game Over."



	def is_collision(self, cameraManager, obstacle):
		# Get some time syncronization checking going on here
		# 	i.e. isStale? within each respective class

		# Also may need collision type - i.e. collisionType() instead of collidesWith()

		if self.obstacle.collides_with(self.cameraManager.get_ball_position(), self.cameraManager.get_ball_radius()):
			return True
		else:
			return False
