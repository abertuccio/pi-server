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

    token = hashlib.sha512(str(mt + random).encode("utf-8")).hexdigest()

    segundos_validez_token = int(time.time()) + \
        (minutos_validez_token_defecto * 60)

    return {"token": token, "tiempo": segundos_validez_token}

def validarToken(token = None):

    if not token:
        raise Error('No se enviaron los parámetros mínimos de autenticación.')

    db = TinyDB('/app/db/usuarios.json')
    Usuario = Query()

    usuario = db.get(Usuario.token.token == token)

    if usuario:
        ahora = int(time.time())
        if ahora < usuario["token"]["tiempo"]:
            return True
    return False

def login(parametros):

    if ("usuario" not in parametros or
            "password" not in parametros):
        raise Error(
            'No se enviaron los parámetros mínimos de autenticación.')

    db = TinyDB('/app/db/usuarios.json')
    Usuario = Query()

    usuario = db.get(Usuario.usuario == parametros["usuario"])

    if not usuario:
        raise Error('La combinacion de usuario y password no es correcta.')

    if usuario["password"] != parametros["password"]:
        raise Error('La combinacion de usuario y password no es correcta..')

    token = generarToken()

    db.update({'token': token}, Usuario.usuario == parametros["usuario"])

    return {"respuesta": token, "status": "Ok"}
