# main

# from CameraManager import CameraManager

# vision = CameraManager()
# vision.startBallTracking()

import time
#from GameManager import GameManager
from ObstacleManager import ObstacleManager
from LaserManager import LaserManager

#game = GameManager()
#game.start_game()

#obstacle = ObstacleManager()
#obstacle.start_movement()

laser = LaserManager()
laser.start()

#obstacle.stop_movement()
while (True):
    #time.sleep(1)
    #obstacle.laserSwitch(input("switch?"))
    userInput = input('Please enter an x and y ("x,y"):')
    if (userInput == "stop"):
        laser.stop()
    laser.setPosition(userInput[0], userInput[1])

