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
        GPIO.setup(2, GPIO.OUT) # vertical servo
        GPIO.setup(14, GPIO.OUT) # horizontal servo
        GPIO.setup(15, GPIO.OUT)  # laser

        self.pwmVert = GPIO.PWM(2, 100)
        self.pwmHori = GPIO.PWM(14, 100)

        self.xPosition = 0
        self.yPosition = 0

        self.properties = Properties()

        self.pwmHori.ChangeDutyCycle(80.0/10 +5)
        #self.pwmVert.ChangeDutyCycle(5)



    def start(self):
        self.pwmVert.start(5)
        self.pwmHori.start(5)
        self.laserSwitch(True)



    # Used by ObstacleManager
    # x and y in meters
    def setPosition(self, x, y):
        self.xPosition = x
        self.yPosition = y

        angles = self.toPolarCoords(self.xPosition, self.yPosition)

        #print("Angles: ", angles)

        dutyhori = float(angles[0] + 90.0) / 10.0 + 5
        dutyvert = float(angles[1]) / 10.0 + 6.72

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

        if myX == 0.0:
            horiAngle = 0.0
        else:
            horiAngle = -math.atan(myX / myY)*180/math.pi  # theta

        vertAngle = math.asin(myZ/math.sqrt(math.pow(myX, 2) + math.pow(myY, 2) + math.pow(myZ, 2))) *180/math.pi  # phi

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



    # turns laser off if false, turns on if true
    def laserSwitch(self, laserOn):
        GPIO.output(15, laserOn)


#    userInput = ''
 #   while (userInput != 'stop'):
  #      userInput = input('Please enter an x and y ("x,y"):')
  #      position = userInput.split(',')#

#        setPosition(position[0], position[1])

 #   stop()
