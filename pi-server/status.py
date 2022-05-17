import requests
import time

def status_aberturas(gp):

    INPUT_ABERTURA_1 = 18
    gp.setup(INPUT_ABERTURA_1, gp.IN, pull_up_down=gp.PUD_UP)

    OUTPUT_ABERTURA = 21 
    gp.setup(OUTPUT_ABERTURA, gp.OUT)

    abertura_abierta = bool(gp.input(INPUT_ABERTURA_1))

    stat = {}
    stat["abertura_abierta"] = abertura_abierta
    return {"status":"Ok","respuesta":stat}