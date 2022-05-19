from tinydb import TinyDB, Query
import RPi.GPIO as GPIO
from status import *
import threading
import time

debe_sonar_alarma = True

def apagaSirena():

    debe_sonar_alarma = False

    GPIO.setmode(GPIO.BCM)

    # Señal de abrir el Relay, Ej: Sirena
    RELAY_220 = 17
    GPIO.setup(RELAY_220, GPIO.OUT) 
    GPIO.output(RELAY_220, GPIO.LOW)

    GPIO.cleanup()
    return "Alarma desarmada"

def enciendeSirena(segundos = 10):
    # if obtenemosPermisoHacerSonar():
    GPIO.setmode(GPIO.BCM)

    # Señal de abrir el Relay, Ej: Sirena
    RELAY_220 = 17
    GPIO.setup(RELAY_220, GPIO.OUT)        
    GPIO.output(RELAY_220, GPIO.HIGH)
    time.sleep(segundos)
    apagaSirena()

def verifica_apertura(intervalo):
    try:
        while True:
            if False:
                debe_sonar_alarma = True
                break
            abertura_abierta = status_aberturas()
            if abertura_abierta:
                notificar_status("APERTURA")
                enciendeSirena()
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("Programa Terminado")
        GPIO.cleanup()

def armar():

    setDebeSonarAlarma(True)

    abertura_abierta = status_aberturas()

    if abertura_abierta:
        res = notificar_status("INTENTO_ARMADO_FALLIDO")
    else:
        res = notificar_status("ARMADO")
        t = threading.Thread(target=verifica_apertura, args=(0.2,))
        t.start()

    return res