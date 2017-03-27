# LaserManager
# UML: https://www.lucidchart.com/documents/edit/e6432d38-782d-40ea-b279-736218c36351/0


import RPi.GPIO as GPIO
import pigpio
import time
import sys
import math

from Properties import Properties


class LaserManager:
    def __init__(self):
        self.DC_LOW = 125000 # Empirically determined duty cycle that gives 0 degrees
        self.DC_HIGH = 475000 # Empirically determined duty cycle that gives 180 degrees
        self.DC_DIFF = self.DC_HIGH - self.DC_LOW  # Difference between high and low dc
        self.PWM_FREQ = 200  # PWM Frequency

        self.HORI_PIN = 19
        self.VERT_PIN = 18
        self.LASER_PIN = 26
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LASER_PIN, GPIO.OUT)  # laser

        self.xPosition = 0
        self.yPosition = 0

        self.properties = Properties()

        self.pi = pigpio.pi()
        self.pi.set_mode(self.VERT_PIN, pigpio.OUTPUT)   # Vertical Servo
        self.pi.set_mode(self.HORI_PIN, pigpio.OUTPUT)   # Horizontal Servo

        self.pi.hardware_PWM(self.VERT_PIN, self.PWM_FREQ, int((self.DC_HIGH+self.DC_LOW)/2))
        self.pi.hardware_PWM(self.HORI_PIN, self.PWM_FREQ, int((self.DC_HIGH+self.DC_LOW)/2))


    # Used by ObstacleManager
    def start(self):
        self.laserSwitch(True)



    # Used by ObstacleManager
    # x and y in meters
    def setPosition(self, x, y):
        self.xPosition = float(x) +0.07
        self.yPosition = float(y)

        #print(x,y)
        
        angles = self.toPolarCoords(self.xPosition, self.yPosition)

        #print("Angles: ", angles)

        dutyhori = ((float(angles[0] + 90.0)/180) * self.DC_DIFF) + self.DC_LOW
        dutyvert = ((float(angles[1] + 15.0)/180) * self.DC_DIFF) + self.DC_LOW

        self.pi.hardware_PWM(self.VERT_PIN, self.PWM_FREQ, int(dutyvert))
        self.pi.hardware_PWM(self.HORI_PIN, self.PWM_FREQ, int(dutyhori))


    # Used by ObstacleManager
    def getXPosition(self):
        return self.xPosition


    # Used by ObstacleManager
    def getYPosition(self):
        return self.yPosition


    # Used by ObstacleManager
    def stop(self):
        self.pi.hardware_PWM(self.HORI_PIN, self.PWM_FREQ, 0)
        self.pi.hardware_PWM(self.VERT_PIN, self.PWM_FREQ, 0)
        self.pi.stop()
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
        GPIO.output(self.LASER_PIN, laserOn)


#    userInput = ''
 #   while (userInput != 'stop'):
  #      userInput = input('Please enter an x and y ("x,y"):')
  #      position = userInput.split(',')#

#        setPosition(position[0], position[1])

 #   stop()
