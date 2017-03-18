# LaserManager
# UML: https://www.lucidchart.com/documents/edit/e6432d38-782d-40ea-b279-736218c36351/0


import RPi.GPIO as GPIO
import time
import sys
import math

from Properties import Properties


class LaserManager:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(2, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        self.pwmVert = GPIO.PWM(2, 100)
        self.pwmHori = GPIO.PWM(18, 100)
        self.pwmVert.start(5)
        self.pwmHori.start(5)

        self.xPosition = 0
        self.yPosition = 0

        self.properties = Properties()

    # Used by ObstacleManager
    def setPosition(self, x, y):
        self.xPosition = x
        self.yPosition = y

        angles = self.toPolarCoords(self.xPosition, self.yPosition)

        dutyhori = float(angles[0]) / 10.0 + 2.5
        dutyvert = float(angles[1]) / 10.0 + 2.5

        self.pwmHori.ChangeDutyCycle(dutyhori)
        self.pwmVert.ChangeDutyCycle(dutyvert)

    # Used by ObstacleManager
    def getXPosition(self):
        return self.xPosition

    # Used by ObstacleManager
    def getYPosition(self):
        return self.yPosition

    # Used by ObstacleManager
    def stop(self):
        self.pwmHori.stop()
        self.pwmVert.stop()
        self.laserSwitch(False)

    def toPolarCoords(self, x, y):
        myX = float(x) - (self.properties.PLAY_FIELD_WIDTH / 2)
        myY = float(y) + self.properties.CAM_DIST_HORI
        myZ = self.properties.CAM_DIST_VERT

        horiAngle = math.atan(myY / myX)  # theta
        vertAngle = math.acos(myY / math.sqrt(math.pow(myX, 2), math.pow(myY, 2), math.pow(myZ, 2)))  # phi

        return horiAngle, vertAngle

    # theta = horizontal angle
    # phi = vertical angle
    def toCartesianCoords(self, theta, phi):
        x = (-(math.tan(theta) / math.pow(math.cos(phi), 2)) + math.sqrt(
            (math.pow(math.tan(theta), 2) / math.pow(math.cos(phi), 4)) - (
            4 + 4 * math.pow(math.tan(theta), 2) * self.properties.CAM_DIST_VERT))) / (
            2 + 2 * math.pow(math.tan(theta), 2))  # Check design logbook p20-21 for equation derivation
        y = x * math.tan(theta)

        return x, y

    def laserSwitch(self, laserOn):
        return laserOn #dummy return so python doesn't complain about an empty def
    #		if laserOn:
    #			time.sleep(1)
    # turn on laser
    #		else:
    #			time.sleep(1)
    # turn off laser


#    userInput = ''
 #   while (userInput != 'stop'):
  #      userInput = input('Please enter an x and y ("x,y"):')
  #      position = userInput.split(',')#

#        setPosition(position[0], position[1])

 #   stop()
