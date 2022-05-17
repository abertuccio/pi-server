from flask import Flask,request,jsonify
from auth import *
from errores.errores import *
import json

app = Flask(__name__, static_folder='app/static',)

@app.route("/")
def main():
    return "El server RPI funciona correctamente"

@app.route("/status")
def status():
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

if __name__ == "__main__":
    # True para desarrollo unicamente
    app.run(host="0.0.0.0", debug=True, port=44306)
