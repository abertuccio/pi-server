import RPi.GPIO as GPIO
import requests
import time

def status_aberturas():

    GPIO.setmode(GPIO.BCM)

    INPUT_ABERTURA_1 = 18
    GPIO.setup(INPUT_ABERTURA_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    OUTPUT_ABERTURA = 21 
    GPIO.setup(OUTPUT_ABERTURA, GPIO.OUT)

    abertura_abierta = bool(GPIO.input(INPUT_ABERTURA_1))

    GPIO.cleanup()

    stat = {}
    stat["abertura_abierta"] = abertura_abierta
    return {"status":"Ok","respuesta":stat}