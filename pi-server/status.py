from tinydb import TinyDB, Query
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import RPi.GPIO as GPIO
import threading
import requests
import time

telegram_URL=""

def setStatusAlarma(status):
    db = TinyDB('/app/db/status.json')
    db.update({"status_alarma":status})

def getStatusAlarma():    
    db = TinyDB('/app/db/status.json')
    # TODO: VER PORQUE SE CORROMPE EL ARCHIVO DE DB
    try:
        status = db.all()[0]['status_alarma']
    except:
        print("Hubo una falla al leer db")

        f = open('/app/db/status.json','r')
        filedata = f.read()
        f.close()

        #{"_default": {"1": {"debe_sonar_alarma": true, "status_alarma": "ARMADO"}}}

        newdata = filedata.replace('^@', '')

        f = open('/app/db/status.json','w')
        f.write(newdata)
        f.close()
            
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

    INPUT_ABERTURA_1 = 20
    GPIO.setup(INPUT_ABERTURA_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    OUTPUT_ABERTURA = 21 
    GPIO.setup(OUTPUT_ABERTURA, GPIO.OUT)

    abertura_abierta = bool(GPIO.input(INPUT_ABERTURA_1))

    return abertura_abierta

def aviso_sonoro(estado):

    # time.sleep(5)

    # GPIO.setmode(GPIO.BCM)
    # GPIO.cleanup()

    BUZZER = 4
    b = TonalBuzzer(BUZZER)    

    if estado == "ARMADO": 

        b.play(Tone("A3"))
        time.sleep(0.3)
        b.stop()
        time.sleep(1) 
        b.play(Tone("A3"))
        time.sleep(0.3)
        b.stop()
        time.sleep(1)

        b.play(Tone("A#3"))
        time.sleep(1)
        b.stop()

    if estado == "NO_ARMADO":        
        b.play(Tone("D4"))
        time.sleep(0.2)
        b.play(Tone("B3"))
        time.sleep(0.5)
        b.play(Tone("D4"))
        time.sleep(0.2)
        b.play(Tone("C#4"))
        time.sleep(0.5)
        b.play(Tone("D4"))
        time.sleep(0.2)
        b.play(Tone("C#4"))
        time.sleep(0.5)
        b.play(Tone("A3"))
        time.sleep(0.6)
        b.stop() 

    if estado == "INTENTO_ARMADO_FALLIDO":

        b.play(Tone("A3"))
        time.sleep(0.3)
        b.stop()
        time.sleep(1) 
        b.play(Tone("A3"))
        time.sleep(0.3)
        b.stop()
        time.sleep(1)

        for x in range(7):
            b.play(Tone("A3"))
            time.sleep(0.2)
            b.stop()
            time.sleep(0.8)
    b.close()


def aviso_de_luces(estado, segundos=0):

        print("Duración del a luz: ",segundos)

        GPIO.setmode(GPIO.BCM)

        ARMADO = 13 # -> ARMADO -> AZUL/BLANCO

        NO_ARMADO = 19 # -> NO ARMADO -> VERDE

        APERTURA = 12 # -> APERTURA/INTENTO_ARMADO_FALLIDO -> ROJO
        
        GPIO.setup(ARMADO, GPIO.OUT)
        GPIO.setup(NO_ARMADO, GPIO.OUT)
        GPIO.setup(APERTURA, GPIO.OUT)
         
        if estado == "ARMADO": # -> ARMADO -> AZUL/BLANCO
            print("Notificación de Armado")
            # GPIO.output(ARMADO,GPIO.HIGH)
            GPIO.output(NO_ARMADO,GPIO.HIGH)
            GPIO.output(APERTURA,GPIO.HIGH)
            GPIO.output(ARMADO, GPIO.LOW)
        if estado == "NO_ARMADO": # -> NO ARMADO -> VERDE
            print("Notificación de Desarmado")
            GPIO.output(ARMADO,GPIO.HIGH)
            # GPIO.output(NO_ARMADO,GPIO.HIGH)
            GPIO.output(APERTURA,GPIO.HIGH)
            GPIO.output(NO_ARMADO, GPIO.LOW)
        if estado == "INTENTO_ARMADO_FALLIDO" or estado == "APERTURA": # -> APERTURA/INTENTO_ARMADO_FALLIDO -> ROJO
            print("Notificación de apertura")
            GPIO.output(ARMADO,GPIO.HIGH)
            GPIO.output(NO_ARMADO,GPIO.HIGH)
            # GPIO.output(APERTURA,GPIO.HIGH)
            GPIO.output(APERTURA, GPIO.LOW)

        if segundos:
            time.sleep(segundos)
        else:
            time.sleep(3000) # <- Máximo de tiempo

        # Apagamos todo
        GPIO.output(ARMADO,GPIO.HIGH)
        GPIO.output(NO_ARMADO,GPIO.HIGH)
        GPIO.output(APERTURA,GPIO.HIGH)        
        
        GPIO.cleanup()

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