import RPi.GPIO as GPIO
import requests
import time

GPIO.setmode(GPIO.BCM)

# Señal de abrir el Relay, Ej: Sirena
RELAY_220 = 17


INPUT_ABERTURA_1 = 18
GPIO.setup(INPUT_ABERTURA_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

OUTPUT_ABERTURA = 21 
GPIO.setup(OUTPUT_ABERTURA, GPIO.OUT)

VERIFICACION = 26
GPIO.setup(VERIFICACION, GPIO.OUT)        
GPIO.output(VERIFICACION, GPIO.HIGH)

TODO_CERRADO = 12
GPIO.setup(TODO_CERRADO, GPIO.OUT)
GPIO.output(TODO_CERRADO, GPIO.LOW)

def obtenemosPermisoHacerSonar():
    id_casa = 1
    permiso_sonar = False
    parametros = {'id': id_casa}
    status_endpoint = "https://vivirconansiedad.com.ar/alarma/status.php"
    r = requests.get(url = status_endpoint, params=parametros)
    status = r.json()
    if status["status"] == "ok":
        permiso_sonar = status["respuesta"]["sonar"]
        print("Permiso de sonar: ", permiso_sonar)
    return permiso_sonar

def todoCerrado():
    abertura_abierta = bool(GPIO.input(INPUT_ABERTURA_1))
    if not abertura_abierta:   
        print("Está todo cerrado, se puede iniciar la alarma")     
        GPIO.output(VERIFICACION, GPIO.LOW)
        GPIO.output(TODO_CERRADO, GPIO.HIGH)
        return True
    print("No está todo cerrado, cierre todo antes de iniciar la alarma.")
    GPIO.output(TODO_CERRADO, GPIO.LOW)
    return False


def enciendeSirena(segundos):
    GPIO.output(TODO_CERRADO, GPIO.LOW)
    if obtenemosPermisoHacerSonar():
        GPIO.setup(RELAY_220, GPIO.OUT)        
        GPIO.output(RELAY_220, GPIO.HIGH)
        time.sleep(segundos)
        apagaSirena()

def apagaSirena():
    GPIO.output(RELAY_220, GPIO.LOW)

def armarAlarma():

    if not todoCerrado():
        time.sleep(10)
        GPIO.cleanup()
        return

    try:
        while True:
            abertura_abierta = bool(GPIO.input(INPUT_ABERTURA_1))

            if abertura_abierta:
                print('Abertura abierta') 
                enciendeSirena(4)
            else:
                print('Todo cerrado')
            time.sleep(0.2) # Tiempo cada cuando se verifica
    except KeyboardInterrupt:
        print("Programa Terminado")
        GPIO.cleanup()

    GPIO.cleanup()

armarAlarma()

