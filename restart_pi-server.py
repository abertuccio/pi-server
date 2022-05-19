from requests.packages.urllib3.exceptions import InsecureRequestWarning
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
cantidad_maxima_intentos = 30

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


telegram_URL="https://api.telegram.org/bot1384549867:AAEx0kR6bAulP6Rnd3_8w0RqMQL9gmDbpDo/sendMessage?chat_id=1072327243"

requests.get(telegram_URL+'&text=Se reinicia RPI, IP: '+ip())

while True:
    print("Verificamos si el server está arriba")
    r = requests.get(rpi_url, verify=False, timeout=5)
    cod = r.status_code
    res = {}
    res["status"] = False

    try:
        res = r.json()
    except:
        pass

    print(res)

    if cod == 200 and res["status"] == 'Ok':
        requests.get(telegram_URL+'&text=El server de la alarma está operativo.')
        print("Está funcionando")
        break

    if not cantidad_maxima_intentos:
        print("Alcanzamos la máxima cantidad de intentos.")
        break

    print("Parece no responder, intentamos levantarlo, Intentos: ",cantidad_maxima_intentos)
    restartTunnel = '/home/pi/telebit restart'
    process = subprocess.Popen(restartTunnel.split(), stdout=subprocess.PIPE)


    cantidad_maxima_intentos = cantidad_maxima_intentos - 1
    time.sleep(20)

