from tinydb import TinyDB, Query
import RPi.GPIO as GPIO
import threading
import requests
import time

telegram_URL="https://api.telegram.org/bot1384549867:AAEx0kR6bAulP6Rnd3_8w0RqMQL9gmDbpDo/sendMessage?chat_id=1072327243"

def setStatusAlarma(status):
    db = TinyDB('/app/db/status.json')
    db.update({"status_alarma":status})

def getStatusAlarma():    
    db = TinyDB('/app/db/status.json')
    status = db.all()[0]['status_alarma']
    t = threading.Thread(target=aviso_de_luces, args=(status,30,))
    t.start()
    return status

def getDdebe_sonar_alarma():    
    db = TinyDB('/app/db/status.json')
    return db.all()[0]['debe_sonar_alarma']

def setDebeSonarAlarma(par):
    db = TinyDB('/app/db/status.json')
    db.update({"debe_sonar_alarma":bool(par)})

def status_aberturas():

    GPIO.setmode(GPIO.BCM)

    INPUT_ABERTURA_1 = 18
    GPIO.setup(INPUT_ABERTURA_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    OUTPUT_ABERTURA = 21 
    GPIO.setup(OUTPUT_ABERTURA, GPIO.OUT)

    abertura_abierta = bool(GPIO.input(INPUT_ABERTURA_1))

    return abertura_abierta

def aviso_de_luces(estado, segundos=0):

        # AZUL/BLANCO -> ARMADO
        # VERDE -> NO ARMADO
        # ROJO -> APERTURA/INTENTO_ARMADO_FALLIDO

        GPIO.setmode(GPIO.BCM)

        GPIO.cleanup()

        NO_ARMADO = 12

        ARMADO = 6

        APERTURA = 26
         
        if estado == "ARMADO":
            GPIO.setup(NO_ARMADO, GPIO.OUT)
            GPIO.output(ARMADO, GPIO.HIGH)
        if estado == "NO_ARMADO":
            GPIO.setup(ARMADO, GPIO.OUT)
            GPIO.output(NO_ARMADO, GPIO.HIGH)
        if estado == "INTENTO_ARMADO_FALLIDO" or "APERTURA":
            GPIO.setup(APERTURA, GPIO.OUT)
            GPIO.output(APERTURA, GPIO.HIGH)

        if segundos:
            time.sleep(segundos)
        else:
            time.sleep(3000) # <- Máximo de tiempo

        # Apagamos todo
        # GPIO.output(NO_ARMADO, GPIO.LOW)
        # GPIO.output(ARMADO, GPIO.LOW)
        # GPIO.output(APERTURA, GPIO.LOW)
        # GPIO.cleanup()

        return

def notificar_status(estado):

    def armado():

        t = threading.Thread(target=aviso_de_luces, args=("ARMADO",0,))
        t.start()

        return("Está todo cerrado, se inicia la alarma.")
    

    def intento_armado_fallido():

        t = threading.Thread(target=aviso_de_luces, args=("INTENTO_ARMADO_FALLIDO",30,))
        t.start()

        return("No está todo cerrado, cierre todo antes de iniciar la alarma.")    

    def no_armado():

        t = threading.Thread(target=aviso_de_luces, args=("NO_ARMADO",0,))
        t.start()

        return("no armado")

    def hubo_una_apertura():

        t = threading.Thread(target=aviso_de_luces, args=("APERTURA",0,))
        t.start()

        # requests.get(telegram_URL+'&text=Se abrió una abertura')

        return("Hubo una apertura.")

    switch_estado = {
	"ARMADO": armado,
	"INTENTO_ARMADO_FALLIDO": intento_armado_fallido,
	"NO_ARMADO": no_armado,
    "APERTURA": hubo_una_apertura
    }

    setStatusAlarma(estado)
    res = switch_estado[estado]()

    return res