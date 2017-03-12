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
		print "Starting Game!!!"
		print "----------------"
		self.cameraManager.start_ball_tracking()
		self.cameraManager.register(self)
		self.obstacle.start_movement()
		self.timeRemaining = 60000
		self.gameOn = True

		while self.gameOn:
			self.timeRemaining -= 1



	def end_game(self):
		print "Game Over."
		self.cameraManager.stop_ball_tracking()
		self.cameraManager.unregister_all()
		self.obstacle.stop_movement()
		self.timeRemaining = 0
		self.gameOn = False



	# Observer function called by any observable class that this class registered to
	def update(self, *args, **keywordargs):

		# TODO: CHECK ARGUMENTS TO DETERMINE MESSAGE/TYPE - pass on to handlers?
		if self.obstacle.collides_with([keywordargs.get('x'), keywordargs.get('y')], self.cameraManager.get_ball_radius()):
			print "------- Collision!!! --------"
			self.end_game()

