# main

# from CameraManager import CameraManager

# vision = CameraManager()
# vision.startBallTracking()

import time
#from GameManager import GameManager
from ObstacleManager import ObstacleManager
#from LaserManager import LaserManager

#game = GameManager()
#game.start_game()

obstacle = ObstacleManager()
obstacle.start_movement()

input('inpuuuuut')
obstacle.stop_movement()
#while (True):
#    time.sleep(1)
    #obstacle.laserSwitch(input("switch?"))
#    userInput = input('Please enter an x and y ("x,y"):')
#    obstacle.setPosition(userInput[0], userInput[1])
