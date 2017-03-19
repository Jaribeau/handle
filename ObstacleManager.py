# Obstacle

import random
import threading
import time

from LaserManager import LaserManager
from Properties import Properties

class ObstacleManager:

    def __init__(self):
        self.xPosition = 0
        self.yPosition = 0
        self.keepMoving = False

        self.speed = 0.5
        self.xSpeed = 0.0
        self.ySpeed = 0.0

        self.xTarget = 0.0
        self.YTarget = 0.0

        self.nextX = 0.0
        self.nextY = 0.0

        self.laser = LaserManager()
        self.properties = Properties()

    # called by GameManager
    def collides_with(self, position, radius):
        x = position[0]
        y = position[1]
        print("Obst: (", self.xPosition, ", ", self.yPosition, ")")
        print("Ball: (", x, ", ", y, ")")
        print("--")
        if (not (0 < x and x < self.properties.PLAY_FIELD_WIDTH and 0 < y and y < self.properties.PLAY_FIELD_LENGTH)):
            return True
        elif ((self.xPosition - radius) <= x <= (self.xPosition + radius)) and (
                (self.yPosition - radius) <= y <= (self.yPosition + radius)):
            return True
        else:
            return False


        # called by GameManager

    def start_movement(self):
        # Start obstacle movement thread
        print("start movement.")
        self.laser.start()
        self.keepMoving = True
        t1 = threading.Thread(target=self.move_obstacle)
        t1.daemon = True
        t1.start()

    # called by GameManager
    def stop_movement(self):
        self.keepMoving = False
        self.laser.stop()
        print("Obstacle motion stopped.")


# Only to be run on its own thread
    def move_obstacle(self):
        while self.keepMoving:  # Random motion until stopMovement called
            # self.xPosition = random.randint(0, 10)
            # self.yPosition = random.randint(0, 10)

            self.nextX = random.random() * self.properties.PLAY_FIELD_WIDTH
            self.nextY = random.random() * self.properties.PLAY_FIELD_LENGTH

            self.laser.setPosition(self.nextX, self.nextY)
            print("New position is", self.nextX, self.nextY)
            time.sleep(1)  # wait 0.75 second
            # self.xPosition = self.nextX
        # self.yPosition = self.nextY

    # Only to be run on its own thread
    #	def next_step(self):
    #		while self.keepMoving:
    #			if (self.xPosition == self.nextX and self.yPosition == self.nextY):
    #                time.sleep(1)


    def set_difficulty(diff):
        if (diff == 0):
            speed = 0.5  # m/s
            # algorithm change?
        else:
            speed = 0.4  # m/s
