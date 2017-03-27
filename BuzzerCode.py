import time
import RPi.GPIO as GPIO

BUZZ_PIN = 21
BUZZ_FREQ = 2000 # Frequency of pulses
dutyCycle = 60 # affects sound frequency
TIME_INTERVAL = 0.5 # time in seconds between buzzes

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZ_PIN, GPIO.OUT)

buzzerPwm = GPIO.PWM(BUZZ_PIN, BUZZ_FREQ) 

buzzerSwitch = True

if buzzerSwitch:
    buzzerPwm.start(self.BUZZ_DC)
    time.sleep(TIME_INTERVAL) # In seconds
    buzzerPwm.stop()
    time.sleep(TIME_INTERVAL)
    buzzerPwm.start(self.BUZZ_DC)
    time.sleep(TIME_INTERVAL)
    buzzerPwm.stop()
    time.sleep(TIME_INTERVAL)
    buzzerPwm.start(self.BUZZ_DC)
    time.sleep(TIME_INTERVAL)
    buzzerPwm.stop()
else:
    buzzerPwm.stop()
        
time.sleep(1)
buzzerSwitch = False
