from tinydb import TinyDB, Query
from errores.errores import *
import hashlib
import pyotp
import time
import os


def html(url):
    html = """<!DOCTYPE html>
                <html>
                <body>
                    <canvas id="qr"></canvas>

                    <script src="static/qrious.js"></script>
                    <script>
                    (function() {
                        var qr = new QRious({
                        element: document.getElementById('qr'),
                        value: '"""+url+"""'
                        });
                    })();
                    </script>
                </body>
                </html>"""
    return(html)


def getQr():
    url = pyotp.totp.TOTP(os.environ['HASH_EMPAREJAMIENTO']).provisioning_uri(
        issuer_name='ALARMA')
    return(html(url))


def getTotp():
    totp = pyotp.TOTP(os.environ['HASH_EMPAREJAMIENTO'])
    return("Current OTP:" + totp.now() + " " + hora)

def generarToken():

    minutos_validez_token_defecto = 20

    mt = str(round(time.time() * 1000))

    random = str(os.urandom(44).hex())

    token = hashlib.sha512( str( mt +  random).encode("utf-8") ).hexdigest()

    segundos_validez_token = int(time.time()) + (minutos_validez_token_defecto * 60)

    return {"token":token,"tiempo":segundos_validez_token}

def login(parametros):

    hash_server = "0012ac79f4559fd080423be618d8ff44c7920f30e73ecf37654041183996fb20"

    if ("hash_server" not in parametros or
        "usuario" not in parametros or
            "password" not in parametros):
        raise Error('No se enviaron los parámetros mínimos de autenticación.')

    if parametros["hash_server"] != hash_server:
        raise Error('No es una ubicación permitida para hacer login.')

    db = TinyDB('/app/db/usuarios.json')
    Usuario = Query()

    usuarioDBD = db.search(Usuario.usuario == parametros["usuario"])

    if not len(usuarioDBD):
        raise Error('La combinacion de usuario y password no es correcta.')

    if usuarioDBD[0]["password"] != parametros["password"]:
        raise Error('La combinacion de usuario y password no es correcta..') 

    token = generarToken()

    db.update({'token': token}, Usuario.usuario == parametros["usuario"])  

    return {"respuesta":token,"status":"Ok"}