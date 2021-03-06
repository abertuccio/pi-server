from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import time
import subprocess
import datetime
import os

conf_env = {}

with open('/home/pi/pi-server/conf/CONF.env', 'r') as fh:        
    for line in fh.readlines(): 
        if not line.startswith('#'):
                var = line.replace('\n', '').split('=',1)
                if len(var) == 2:
                    conf_env[var[0]]=var[1]

path_telebid = '/home/pi/'

print(datetime.datetime.now()," Restarteamos Docker")

restartDocker = "docker restart pi-server"
process = subprocess.Popen(restartDocker.split(), stdout=subprocess.PIPE)
outs, errs = process.communicate()

print(datetime.datetime.now()," Docker iniciado: ", str(outs))
print(datetime.datetime.now()," Errores: ",errs)

print(datetime.datetime.now()," Esperamos 20 segudos para intentar telebit")
time.sleep(20)

rpi_url = 'https://stale-octopus-48.telebit.io/'
cantidad_maxima_intentos = 30

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


telegram_URL=conf_env['TELEGRAM_URL']

requests.get(telegram_URL+'&text=Se reinicia RPI, IP: '+ip())

while True:
    print(datetime.datetime.now()," Verificamos si el server está arriba")
    cod = 500
    try:
        r = requests.get(rpi_url+'status_interno?hash=2fc76d29016f0eb3d9b041cfbe8c13db777973cc6bf6b2c9463727e090d51a1a', verify=False, timeout=5)
        cod = r.status_code
    except:
        pass
    res = {}
    res["status"] = False

    try:
        res = r.json()
    except:
        pass

    print(res)

    if cod == 200 and res["status"] == 'Ok':
        requests.get(telegram_URL+'&text=El server de la alarma está operativo.')
        print(res["respuesta"]['status_alarma'])
        if res["respuesta"]['status_alarma'] == "ARMADO":
            # Intentamos armar nuevamente
            print("Se intenta armar")
            r = requests.get(rpi_url+'armar_interno?hash=2fc76d29016f0eb3d9b041cfbe8c13db777973cc6bf6b2c9463727e090d51a1a', verify=False, timeout=5)
            res = r.json()
            status_armar_server = "Hubo un error al armar"
            if "respuesta" in res and "server" in res["respuesta"]:
                status_armar_server = res["respuesta"]["server"]
            requests.get(telegram_URL+'&text=Hubo un corte y se intentó armar. Respuesta del servidor: '+status_armar_server)   
        print(datetime.datetime.now()," Está funcionando")
        break

    if not cantidad_maxima_intentos:
        print(datetime.datetime.now()," Alcanzamos la máxima cantidad de intentos.")
        break

    print(datetime.datetime.now()," Parece no responder, intentamos levantarlo, Intentos: ",cantidad_maxima_intentos)
    restartTunnel = '/home/pi/telebit restart'
    process = subprocess.Popen(restartTunnel.split(), stdout=subprocess.PIPE)


    cantidad_maxima_intentos = cantidad_maxima_intentos - 1
    time.sleep(20)


