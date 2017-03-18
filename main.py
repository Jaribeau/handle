# main

# from CameraManager import CameraManager

# vision = CameraManager()
# vision.startBallTracking()


#from GameManager import GameManager
from ObstacleManager import ObstacleManager

#game = GameManager()
#game.start_game()

obstacle = ObstacleManager()
obstacle.start_movement()

input('stop?')