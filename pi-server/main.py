from flask_cors import CORS, cross_origin
from flask import Flask,request,jsonify
from errores.errores import *
from status import *
from auth import *
from armar import *
import subprocess
import threading
import time
import json

app = Flask(__name__, static_folder='app/static',)
CORS(app)
app.config['CORS_HEADERS'] = 'application/json'

@app.route("/", methods = ['GET'])
@cross_origin()
def main():
    return {"status":"Ok","respuesta":"El server RPI funciona correctamente"}

@app.route("/status", methods = ['GET'])
@cross_origin()
def status_fn():
    token = request.args.get('token', default = False)
    
    if not validarToken(token):
        raise Error('Debe volver a loguearse.')

    stat = {}
    stat["server"] = "El server RPI funciona correctamente"
    stat["abertura_abierta"] = status_aberturas()
    stat["status_alarma"] = getStatusAlarma()

    return {"status":"Ok","respuesta":stat}

@app.route("/login", methods = ['POST'])
@cross_origin()
def login_fn():
    content = request.json

    return login(content)

@app.route("/armar", methods = ['GET'])
@cross_origin()
def armar_fn():
    token = request.args.get('token', default = False)

    if not validarToken(token):
        raise Error('Debe volver a loguearse.')

    stat = {}
    stat["server"] = armar()

    return {"status":"Ok","respuesta":stat}

@app.route("/desarmar", methods = ['GET'])
@cross_origin()
def desarmar_fn():
    token = request.args.get('token', default = False)

    if not validarToken(token):
        raise Error('Debe volver a loguearse.')

    stat = {}
    stat["server"] = desarmar()

    return {"status":"Ok","respuesta":stat}

# @app.route("/qr", methods = ['GET'])
# def qr_fn():
#     return getQr()

# @app.route("/totp", methods = ['GET'])
# def totp_fn():
#     return getTotp()

@app.errorhandler(Error)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response

@app.after_request
def after_request_func(response):

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=44306)
