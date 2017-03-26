import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENTER NUMBER, GPIO.OUT)

buzzerPwm = GPIO.PWM(ENTER NUMBER, 100)
p.start(0)