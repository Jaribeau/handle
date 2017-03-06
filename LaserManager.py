# LaserManager
# UML: https://www.lucidchart.com/documents/edit/e6432d38-782d-40ea-b279-736218c36351/0


import RPi.GPIO as GPIO
import time
import sys
import math

xPosition = 0
yPosition = 0

global def setPosition(x, y):
	# Do stuff

global def getXPosition():
	return xPosition

global def getYPosition():
	return yPosition

PLAY_FIELD_WIDTH = 2
PLAY_FIELD_LENGTH = 2
CAM_DIST_HORI = 0.5
CAM_DIST_VERT = 1.5

if (len(sys.argv) != 2):
    print 'Please input 2 arguments, the x position and y position as arguments.'
    quit()
else:
    x = sys.argv[1]
    y = sys.argv[2]


myX = X - (PLAY_FIELD_WIDTH/2)
myY = y + CAM_DIST_HORI
myZ = CAM_DIST_VERT

horiAngle = math.atan(myY/myX)
vertAngle = math.acos(myY/math.sqrt(pow(myX,2),pow(myY,2),pow(myZ,2)))

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
pwm = GPIO.PWM(2, 100)
pwm.start(5)


    duty = float(angle) / 10.0 + 2.5
    pwm.ChangeDutyCycle(duty)


pwm.stop()
