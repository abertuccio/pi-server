import requests
import time

def status_aberturas(gp):

    INPUT_ABERTURA_1 = 18
    gp.setup(INPUT_ABERTURA_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    OUTPUT_ABERTURA = 21 
    gp.setup(OUTPUT_ABERTURA, GPIO.OUT)

    abertura_abierta = bool(gp.input(INPUT_ABERTURA_1))

    stat = {}
    stat["abertura_abierta"] = abertura_abierta
    return {"status":"Ok","respuesta":stat}