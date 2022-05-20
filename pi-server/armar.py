from tinydb import TinyDB, Query
import RPi.GPIO as GPIO
from status import *
import threading
import time


def desarmar():
    setDebeSonarAlarma(False)

    time.sleep(5)

    setStatusAlarma("NO_ARMADO")

    return apagaSirena()

def apagaSirena():

    GPIO.setmode(GPIO.BCM)

    # Señal de abrir el Relay, Ej: Sirena
    RELAY_220 = 17
    GPIO.setup(RELAY_220, GPIO.OUT) 
    GPIO.output(RELAY_220, GPIO.LOW)

    GPIO.cleanup()
    return "Alarma desarmada"

def enciendeSirena(segundos = 30):
    # if obtenemosPermisoHacerSonar():
    print("La alarma sonará: ",segundos," segundos")

    GPIO.setmode(GPIO.BCM)

    # Señal de abrir el Relay, Ej: Sirena
    RELAY_220 = 17
    GPIO.setup(RELAY_220, GPIO.OUT)        
    GPIO.output(RELAY_220, GPIO.HIGH)
    time.sleep(segundos)
    # apagaSirena()

def verifica_apertura(intervalo):
        while True:
            if not getDdebe_sonar_alarma():
                setDebeSonarAlarma(True)
                break
            abertura_abierta = status_aberturas()
            if abertura_abierta:
                # notificar_status("APERTURA")
                enciendeSirena()
            time.sleep(intervalo)

def armar():

    setDebeSonarAlarma(True)

    abertura_abierta = status_aberturas()

    if getStatusAlarma() == "ARMADO":
        res = notificar_status("ARMADO")
    return res

    if abertura_abierta:
        res = notificar_status("INTENTO_ARMADO_FALLIDO")
    else:
        res = notificar_status("ARMADO")
        t = threading.Thread(target=verifica_apertura, args=(0.2,))
        t.start()

    return res