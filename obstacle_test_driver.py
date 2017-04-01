
from ObstacleManager import ObstacleManager
import time

obstacle = ObstacleManager.get_instance()
obstacle.start_movement()
obstacle.set_period(0.05)

start_time = time.clock()
while time.clock() - start_time < 3:
    print("Obstacle Position: (" + str(obstacle.xPosition) + ", " + str(obstacle.yPosition) + ")")

obstacle.stop_movement()
