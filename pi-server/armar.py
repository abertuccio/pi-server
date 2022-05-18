import RPi.GPIO as GPIO
from status import *


def armar():

    abertura_abierta = status_aberturas()

    if abertura_abierta:
        res = notificar_status("INTENTO_ARMADO_FALLIDO")
    else:
        res = notificar_status("ARMADO")

    return res