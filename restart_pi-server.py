import requests
import time
import subprocess

path_telebid = '/home/pi/'

print("Restarteamos Docker")

restartDocker = "docker restart pi-server"
process = subprocess.Popen(restartDocker.split(), stdout=subprocess.PIPE)
outs, errs = process.communicate()

print(outs)
print(errs)

print("Esperamos 20 segudos para intentar telebit")
time.sleep(20)

rpi_url = 'https://light-panda-16.telebit.io/status'
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

    if cod == 200 and res["status"] == 'Ok' and cantidad_maxima_intentos > 0:
        print("Está funcionando")
        break
    
    print("Intentamos levantarlo")
    restartTunnel = "telebit restart"
    process = subprocess.Popen(restartTunnel.split(), stdout=subprocess.PIPE,cwd=path_telebid)
    cantidad_maxima_intentos = cantidad_maxima_intentos - 1
    time.sleep(10)
