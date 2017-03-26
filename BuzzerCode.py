import time
import RPi.GPIO as GPIO

dutyCycle = 15 # affects sound frequency

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

buzzerPwm = GPIO.PWM(21, 2000)

buzzerSwitch = True

if buzzerSwitch:
    buzzerPwm.start(60)
    time.sleep(0.5)
    buzzerPwm.stop()
    time.sleep(0.5)
    buzzerPwm.start(60)
    time.sleep(0.5)
    buzzerPwm.stop()
    time.sleep(0.5)
    buzzerPwm.start(60)
    time.sleep(0.5)
    buzzerPwm.stop()
else:
    buzzerPwm.stop()
        
time.sleep(1)
buzzerSwitch = False
