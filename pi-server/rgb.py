import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

LED_ROJO = 13
LED_VERDE = 6
LED_VERDE = 26

GPIO.setup(LED_ROJO, GPIO.OUT)
GPIO.output(LED_ROJO, GPIO.HIGH)
time.sleep(2)
GPIO.output(LED_ROJO, GPIO.LOW)

GPIO.cleanup()