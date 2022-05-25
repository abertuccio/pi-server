import RPi.GPIO as GPIO
import time

BUZZER = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.output(BUZZER, GPIO.HIGH)

time.sleep(1)

GPIO.output(BUZZER, GPIO.LOW)
GPIO.cleanup()