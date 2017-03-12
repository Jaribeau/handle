# GameManager

from CameraManager import CameraManager
from Obstacle import Obstacle

class GameManager:


	def __init__(self):
		self.cameraManager = CameraManager()
		self.obstacle = Obstacle()
		self.timeRemaining = 60000
		self.gameOn = False



	def startGame(self):
		self.cameraManager.startBallTracking()
		self.obstacle.startMovement()
		self.timeRemaining = 60000
		self.gameOn = True


		print "Starting Game!!!"
		print "----------------"

		while self.gameOn:

			if self.isCollision(self.cameraManager, self.obstacle):
				print "------- Collision!!! --------"
				self.gameOn = False

			else:
				print "."

		print "Game Over."



	def isCollision( self, cameraManager, obstacle):
		# Get some time syncronization checking going on here
		# 	i.e. isStale? within each respective class

		# Also may need collision type - i.e. collisionType() instead of collidesWith()

		if self.obstacle.collidesWith( self.cameraManager.getBallPosition(), self.cameraManager.getBallRadius() ):
			return True
		else:
			return False
