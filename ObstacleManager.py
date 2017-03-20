# Obstacle

import random
import threading
import time

from LaserManager import LaserManager
from Properties import Properties
from BallTracker import BallTracker

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

        self.mode = "follow"

        self.laser = LaserManager()
        self.properties = Properties()
        self.ballTracker = BallTracker()


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

            # if (self.mode== "follow"):
            #     self.nextX = self.nextX
            #     self.nextY = self.nextY
            # elif (self.mode == random):
            #     self.nextX = random.random() * self.properties.PLAY_FIELD_WIDTH
            #     self.nextY = random.random() * self.properties.PLAY_FIELD_LENGTH


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

    # Observer function called by any observable class that this class registered to
    def notify(self, *args, **keywordargs):
        # TODO: CHECK ARGUMENTS TO DETERMINE MESSAGE/TYPE - pass on to handlers?
        self.nextX = keywordargs.get('x')
        self.nextY = keywordargs.get('y')

    def set_mode(self, newMode):
        self.mode = newMode
        if newMode == "follow":
            self.ballTracker.register(self)
        else:
            self.ballTracker.unregister(self)
