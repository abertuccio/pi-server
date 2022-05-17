import RPi.GPIO as GPIO
import threading
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

    return abertura_abierta

def notificar_status(estado):

    GPIO.setmode(GPIO.BCM)
    TODO_CERRADO = 12
    GPIO.setup(TODO_CERRADO, GPIO.OUT)
    VERIFICACION = 26
    GPIO.setup(VERIFICACION, GPIO.OUT)

    # Apagamos todo
    GPIO.output(VERIFICACION, GPIO.LOW)
    GPIO.output(TODO_CERRADO, GPIO.LOW)

    # threads = list()

    def luces(verificacion=False,todo_cerrado=False, segundos=5):
        
        if verificacion:
            GPIO.output(VERIFICACION, GPIO.HIGH)
        else:
            GPIO.output(VERIFICACION, GPIO.LOW)

        if todo_cerrado:
            GPIO.output(TODO_CERRADO, GPIO.HIGH)
        else:
            GPIO.output(TODO_CERRADO, GPIO.LOW)
        time.sleep(segundos)

        GPIO.cleanup()

    def armado():
        return("armado")

    def intento_armado_fallido():

        t = threading.Thread(target=luces, args=(True,False,5))
        # threads.append(t) 
        [t].start()
        
        return("No está todo cerrado, cierre todo antes de iniciar la alarma.")

    def no_armado():        
        return("no armado")

    switch_estado = {
	"ARMADO": armado,
	"INTENTO_ARMADO_FALLIDO": intento_armado_fallido,
	"NO_ARMADO": no_armado
    }

    res = switch_estado[estado]()

    GPIO.cleanup()

    return res