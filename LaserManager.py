# LaserManager
# UML: https://www.lucidchart.com/documents/edit/e6432d38-782d-40ea-b279-736218c36351/0


import RPi.GPIO as GPIO
import time
import sys
import math

PLAY_FIELD_WIDTH = 2
PLAY_FIELD_LENGTH = 2
CAM_DIST_HORI = 0.5
CAM_DIST_VERT = 1.5

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
pwmVert = GPIO.PWM(2, 100)
pwmHori = GPIO.PWM(18, 100)
pwmVert.start(5)
pwmHori.start(5)

xPosition = 0
yPosition = 0

global def setPosition(x, y):
	xPosition = x
	yPosition = y

	angles = toPolarCoords(xPosition, yPosition)

	dutyhori = float(angles[0]) / 10.0 + 2.5
	dutyvert = float(angles[1]) / 10.0 + 2.5

	pwmHori.ChangeDutyCycle(dutyhori)
	pwmVert.ChangeDutyCycle(dutyvert)

global def getXPosition():
	return xPosition

global def getYPosition():
	return yPosition

global def stop():
	pwmHori.stop()
	pwmVert.stop()



def toPolarCoords(x,y):
	myX = float(x) - (PLAY_FIELD_WIDTH/2)
	myY = float(y) + CAM_DIST_HORI
	myZ = CAM_DIST_VERT

	horiAngle = math.atan(myY/myX) # theta
	vertAngle = math.acos(myY/math.sqrt(math.pow(myX,2),math.pow(myY,2),math.pow(myZ,2))) # phi

	return horiAngle,vertAngle

# theta = horizontal angle
# phi = vertical angle
def toCartesianCoords(theta, phi):
	x = (-(math.tan(theta)/math.pow(math.cos(phi),2)) + math.sqrt((math.pow(math.tan(theta),2)/math.pow(math.cos(phi),4)) - (4 + 4*math.pow(math.tan(theta),2)*CAM_DIST_VERT)))/(2+2*math.pow(math.tan(theta),2)) # Check design logbook p20-21 for equation derivation
	y = x*math.tan(theta)

	return x,y

userInput = ''
while (userInput != 'stop'):
	userInput = input('Please enter an x and y ("x,y"):')
	position = userInput.split(',')

	setPosition(position[0], position[1])

stop()