import requests
import time
import subprocess

path_telebid = '/home/pi/'

restartDocker = "docker restart pi-server"
process = subprocess.Popen(restartDocker.split(), stdout=subprocess.PIPE)

time.sleep(20)

rpi_url = 'https://light-panda-16.telebit.io/status'
cantidad_maxima_intentos = 100

while True:
    print("Verificamos si el server está arriba")
    r = requests.get(rpi_url)
    cod = r.status_code
    res = r.json()

    if cod == 200 and res["status"] == 'Ok' and cantidad_maxima_intentos > 0:
        print("Está funcionando")
        break
    
    print("Intentamos levantarlo")
    restartTunnel = "telebit restart"
    process = subprocess.Popen(restartTunnel.split(), stdout=subprocess.PIPE,cwd=path_telebid)
    cantidad_maxima_intentos = cantidad_maxima_intentos - 1
    time.sleep(10)

