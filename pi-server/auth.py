from errores.errores import *
from login.LoginApisews import LoginApisews
import pyotp
import time


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
    url = pyotp.totp.TOTP('JBSWY3DPEHPK3PXP').provisioning_uri(
        issuer_name='ALARMA')
    return(html(url))


def getTotp(usuarioSecret, param):
    totp = pyotp.TOTP(usuarioSecret)
    return("Current OTP:" + totp.now() + " " + hora)