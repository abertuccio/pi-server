import RPi.GPIO as GPIO
from status import *


def armar():

    print("Se ejecuta armar")

    abertura_abierta = status_aberturas()

    if abertura_abierta:
        res = notificar_status("INTENTO_ARMADO_FALLIDO")

    return res