import time
import RPi.GPIO as GPIO

BUZZ_PIN = 21
BUZZ_FREQ = 2000 # Frequency of pulses
dutyCycle = 60 # affects sound frequency

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZ_PIN, GPIO.OUT)

buzzerPwm = GPIO.PWM(BUZZ_PIN, BUZZ_FREQ) 

buzzerSwitch = True

if buzzerSwitch:
    buzzerPwm.start(dutyCycle)
    time.sleep(0.5) # In seconds
    buzzerPwm.stop()
    time.sleep(0.5)
    buzzerPwm.start(dutyCycle)
    time.sleep(0.5)
    buzzerPwm.stop()
    time.sleep(0.5)
    buzzerPwm.start(dutyCycle)
    time.sleep(0.5)
    buzzerPwm.stop()
else:
    buzzerPwm.stop()
        
time.sleep(1)
buzzerSwitch = False
