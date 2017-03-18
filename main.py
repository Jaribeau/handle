# main

# from CameraManager import CameraManager

# vision = CameraManager()
# vision.startBallTracking()

import time
#from GameManager import GameManager
from ObstacleManager import ObstacleManager

#game = GameManager()
#game.start_game()

obstacle = ObstacleManager()
obstacle.start_movement()

while (True):
    time.sleep(1)