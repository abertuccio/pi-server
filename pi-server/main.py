from flask import Flask,request,jsonify
from errores.errores import *
import RPi.GPIO as GPIO
from status import *
from auth import *
import json

GPIO.setmode(GPIO.BCM)

app = Flask(__name__, static_folder='app/static',)

@app.route("/")
def main():
    return "El server RPI funciona correctamente"

@app.route("/status")
def status():
    stat = {}
    stat["server"] = "El server RPI funciona correctamente"
    stat["status_aberturas"] = status_aberturas(GPIO)
    return {"status":"Ok","respuesta":stat}

@app.route("/armar")
def armar():
    stat = {}
    stat["server"] = "El server RPI funciona correctamente"
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
