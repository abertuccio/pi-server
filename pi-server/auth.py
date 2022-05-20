from errores.errores import *
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