from tinydb import TinyDB, Query
import RPi.GPIO as GPIO
import threading
import requests
import time

def getDdebe_sonar_alarma():
    
    db = TinyDB('pi-server/db.json')
    db.insert({'debe_sonar_alarma': True})

def setDebeSonarAlarma(bool):
    db = TinyDB('pi-server/db.json')
    db.insert({'debe_sonar_alarma': bool})

def status_aberturas():

    GPIO.setmode(GPIO.BCM)

    INPUT_ABERTURA_1 = 18
    GPIO.setup(INPUT_ABERTURA_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    OUTPUT_ABERTURA = 21 
    GPIO.setup(OUTPUT_ABERTURA, GPIO.OUT)

    abertura_abierta = bool(GPIO.input(INPUT_ABERTURA_1))

    GPIO.cleanup()

    return abertura_abierta

def aviso_de_luces(verificacion=False,todo_cerrado=False, segundos=0):

        GPIO.setmode(GPIO.BCM)

        TODO_CERRADO = 12
        GPIO.setup(TODO_CERRADO, GPIO.OUT)

        VERIFICACION = 26
        GPIO.setup(VERIFICACION, GPIO.OUT)

        # Apagamos todo
        GPIO.output(VERIFICACION, GPIO.LOW)
        GPIO.output(TODO_CERRADO, GPIO.LOW)
        
        if verificacion:
            GPIO.output(VERIFICACION, GPIO.HIGH)
        else:
            GPIO.output(VERIFICACION, GPIO.LOW)

        if todo_cerrado:
            GPIO.output(TODO_CERRADO, GPIO.HIGH)
        else:
            GPIO.output(TODO_CERRADO, GPIO.LOW)

        if segundos:
            time.sleep(segundos)
            GPIO.cleanup()
        else:
            time.sleep(1200)
            GPIO.cleanup()

        return

def notificar_status(estado):

    def armado():
        t = threading.Thread(target=aviso_de_luces, args=(False,True,0,))
        t.start()

        return("Está todo cerrado, se puede iniciar la alarma")
    

    def intento_armado_fallido():

        t = threading.Thread(target=aviso_de_luces, args=(True,False,5,))
        t.start()

        return("No está todo cerrado, cierre todo antes de iniciar la alarma.")    

    def no_armado():        
        return("no armado")

    def hubo_una_apertura():

        t = threading.Thread(target=aviso_de_luces, args=(True,False,5,))
        t.start()

        # Enviar mensaje

        return("Hubo una apertura.")

    switch_estado = {
	"ARMADO": armado,
	"INTENTO_ARMADO_FALLIDO": intento_armado_fallido,
	"NO_ARMADO": no_armado,
    "APERTURA": hubo_una_apertura
    }

    res = switch_estado[estado]()

    return res