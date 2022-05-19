import requests
import time
import subprocess

path_telebid = '/home/pi/'

print("Restarteamos Docker")

restartDocker = "docker restart pi-server"
process = subprocess.Popen(restartDocker.split(), stdout=subprocess.PIPE)
outs, errs = process.communicate()

print("Docker iniciado: ", str(outs))
print("Errores: ",errs)

print("Esperamos 20 segudos para intentar telebit")
time.sleep(20)

rpi_url = 'https://stale-octopus-48.telebit.io/status'
cantidad_maxima_intentos = 100

while True:
    print("Verificamos si el server está arriba")
    r = requests.get(rpi_url, verify=False)
    cod = r.status_code
    res = {}
    res["status"] = False

    try:
        res = r.json()
    except:
        pass

    print(res)

    if cod == 200 and res["status"] == 'Ok':
        print("Está funcionando")
        break

    if not cantidad_maxima_intentos:
        print("Alcanzamos la máxima cantidad de intentos.")
        break

    print("Parece no responder, intentamos levantarlo, Intentos: ",cantidad_maxima_intentos)
    restartTunnel = '/home/pi/telebit restart'
    # process = subprocess.Popen(restartTunnel.split(), stdout=subprocess.PIPE,cwd="/home/pi")
    process = subprocess.Popen(restartTunnel.split(), stdout=subprocess.PIPE)


    cantidad_maxima_intentos = cantidad_maxima_intentos - 1
    time.sleep(10)

