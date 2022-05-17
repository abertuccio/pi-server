from flask import Flask,request,jsonify
from errores.errores import *
import RPi.GPIO as GPIO
from status import *
from auth import *
from armar import *
import json

app = Flask(__name__, static_folder='app/static',)

@app.route("/")
def main():
    return "El server RPI funciona correctamente"

@app.route("/status")
def status_fn():
    stat = {}
    stat["server"] = "El server RPI funciona correctamente"
    stat["abertura_abierta"] = status_aberturas()
    return {"status":"Ok","respuesta":stat}

@app.route("/armar")
def armar_fn():
    stat = {}
    stat["server"] = armar()
    return {"status":"Ok","respuesta":stat}

@app.route("/qr")
def qr():
    return getQr()


@app.route("/totp")
def totp():
    return getTotp()

@app.errorhandler(Error)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.after_request
def after_request_func(response):
    GPIO.cleanup()
    return response

if __name__ == "__main__":
    # True para desarrollo unicamente
    app.run(host="0.0.0.0", debug=True, port=44306)
