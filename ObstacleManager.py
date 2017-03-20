# Obstacle

import random
import threading
import time
import math

from LaserManager import LaserManager
from Properties import Properties
from BallTracker import BallTracker

class ObstacleManager:

    def __init__(self):
        self.xPosition = 0
        self.yPosition = 0
        self.keepMoving = False

        self.speed = 0.01

        self.xTarget = 0.0
        self.yTarget = 0.0

        self.nextX = 0.0
        self.nextY = 0.0

        self.mode = "target"
        self.set_mode("target")
        self.period = 0.2 # millisecond between each movement

        self.laser = LaserManager()
        self.properties = Properties()
        self.ballTracker = BallTracker.get_instance()


    # called by GameManager
    def collides_with(self, position, radius):
        x = float(position[0])/100.0 # Converting cm to m
        y = float(position[1])/100.0 # Converting cm to m
        print("Obst: (", self.xPosition, ", ", self.yPosition, ")")
        print("Ball: (", x, ", ", y, ")")
        print("--")
        #if (not (0 < x and x < self.properties.PLAY_FIELD_WIDTH and 0 < y and y < self.properties.PLAY_FIELD_LENGTH)):
        #    return True
        if ((self.xPosition - radius) <= x <= (self.xPosition + radius)) and (
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
            print(self.mode)
            if (self.mode== "target"):
                if self.xTarget == self.xPosition and self.yTarget == self.yPosition:
                    self.xTarget = random.random() * self.properties.PLAY_FIELD_WIDTH
                    self.yTarget = random.random() * self.properties.PLAY_FIELD_LENGTH
            elif (self.mode == "random"):
                self.xTarget = random.random() * self.properties.PLAY_FIELD_WIDTH
                self.yTarget = random.random() * self.properties.PLAY_FIELD_LENGTH

            self.speed_calc()

            self.laser.setPosition(self.nextX, self.nextY)
            self.xPosition = self.nextX
            self.yPosition = self.nextY
            #print("New position is", self.nextX, self.nextY)
            time.sleep(self.period)  # wait this many seconds
            # self.xPosition = self.nextX
        # self.yPosition = self.nextY

    def speed_calc(self):
        print("Target" , self.xTarget, self.yTarget)
        print("Position" , self.xPosition, self.yPosition)
        xDiff = self.xTarget - self.xPosition
        yDiff = self.yTarget - self.yPosition
        maxDisp = self.speed * self.period
        if (math.sqrt(math.pow(xDiff,2) + math.pow(yDiff,2)) > maxDisp):
            angle = math.tan(yDiff/xDiff)
            self.nextX = self.nextX + (maxDisp*math.cos(angle))
            self.nextY = self.nextY + (maxDisp*math.sin(angle))
        else:
            self.nextX = self.xTarget
            self.nextY = self.yTarget

    # Only to be run on its own thread
    #	def next_step(self):
    #		while self.keepMoving:
    #			if (self.xPosition == self.nextX and self.yPosition == self.nextY):
    #                time.sleep(1)

    # Observer function called by any observable class that this class registered to
    def notify(self, *args, **keywordargs):
        # TODO: CHECK ARGUMENTS TO DETERMINE MESSAGE/TYPE - pass on to handlers?
        if self.mode == "follow":
            self.xTarget = keywordargs.get('x')
            self.yTarget = keywordargs.get('y')


    # Possible modes: "follow", "target", "random"
    def set_mode(self, newMode):
        if newMode == "follow" and self.mode != "follow":
            self.ballTracker.register(self)
        elif newMode != "follow" and self.mode == "follow":
            self.ballTracker.unregister(self)

        self.mode = newMode

    def set_speed(self, newSpeed):
        self.speed = newSpeed