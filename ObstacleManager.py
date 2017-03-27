# Obstacle

import random
import threading
import time
import math

from LaserManager import LaserManager
from Properties import Properties
from BallTracker import BallTracker


class ObstacleManager:


    # Singleton instance
    instance = None


    @staticmethod
    def get_instance():
        if ObstacleManager.instance is None:
            ObstacleManager.instance = ObstacleManager()

        return ObstacleManager.instance


    def __init__(self):
        self.laser = LaserManager()
        self.properties = Properties()
        self.ballTracker = BallTracker.get_instance()

        self.xPosition = 50
        self.yPosition = 50
        self.keepMoving = False

        self.speed = 0.01

        self.xTarget = 0.0
        self.yTarget = 0.0

        self.nextX = 50
        self.nextY = 50

        self.x_rate = 1
        self.y_rate = 1

        self.mode = "bounce"
        self.set_mode(self.mode)
        self.period = 0.04  # seconds between each movement

        # Singleton logic
        if ObstacleManager.instance is None:
            ObstacleManager.instance = self
        else:
            print("WARNING: You are creating an instance directly in a class intended to be a singleton. "
                  "Use BallTracker.get_instance() instead.")


        # Check if outside of play area
        #if (not (0 < x and x < self.properties.PLAY_FIELD_WIDTH and 0 < y and y < self.properties.PLAY_FIELD_LENGTH)):
        #    return True



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

        #print("Obstacle mode:", self.mode)

        while self.keepMoving:  # Random motion until stopMovement called

            if self.mode == "fixed":
                self.nextX = self.properties.GRID_SIZE_X / 2
                self.nextY = self.properties.GRID_SIZE_Y / 2


            elif self.mode == "target":
                if self.xTarget == self.xPosition and self.yTarget == self.yPosition:
                    self.xTarget = random.random() * self.properties.PLAY_FIELD_WIDTH
                    self.yTarget = random.random() * self.properties.PLAY_FIELD_LENGTH
                    self.speed_calc()


            elif self.mode == "random":
                self.xTarget = random.random() * self.properties.PLAY_FIELD_WIDTH
                self.yTarget = random.random() * self.properties.PLAY_FIELD_LENGTH
                self.speed_calc()


            elif self.mode == "bounce":
                if self.xPosition < 0:
                    self.x_rate = (random.randint(1, 3))
                    self.y_rate = (random.randint(-3, 3))

                elif self.xPosition > self.properties.GRID_SIZE_X:
                    self.x_rate = -(random.randint(1, 3))
                    self.y_rate = (random.randint(-3, 3))

                elif self.yPosition < 0:
                    self.x_rate = (random.randint(-3, 3))
                    self.y_rate = (random.randint(1, 3))

                elif self.yPosition > self.properties.GRID_SIZE_Y:
                    self.x_rate = -(random.randint(-3, 3))
                    self.y_rate = -(random.randint(1, 3))

                self.nextX = self.xPosition + self.x_rate
                self.nextY = self.yPosition + self.y_rate


            self.laser.setPosition(self.nextX / float(Properties.GRID_SIZE_X), self.nextY / float(Properties.GRID_SIZE_Y))
            self.xPosition = self.nextX
            self.yPosition = self.nextY
            time.sleep(self.period)  # wait this many seconds



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



    # Observer function called by any observable class that this class registered to
    def notify(self, *args, **keywordargs):
        # TODO: CHECK ARGUMENTS TO DETERMINE MESSAGE/TYPE - pass on to handlers?
        if self.mode == "follow" and keywordargs.get('x') != None and keywordargs.get('y')!= None:
            self.nextX = keywordargs.get('x')/100.0
            self.nextY = keywordargs.get('y')/100.0


    # Possible modes: "follow", "target", "random"
    def set_mode(self, newMode):
        if newMode == "follow" and self.mode != "follow":
            self.ballTracker.register(self)
        elif newMode != "follow" and self.mode == "follow":
            self.ballTracker.unregister(self)

        self.mode = newMode

    def set_speed(self, newSpeed):
        self.speed = newSpeed
