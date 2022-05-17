import RPi.GPIO as GPIO
import time

import pyIR.pyIR as pyIR

IR = 32

mySensor = pyIR.Receiver(IR)

try:
    while True:
        data = mySensor.getRAW()
        print(data)
        time.sleep(0.2) # Tiempo cada cuando se verifica
except KeyboardInterrupt:
    print("Programa Terminado")
    