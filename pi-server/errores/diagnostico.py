# dig +short x-desarrollo.sintys.gob.ar
# systemd-resolve google.com

import os

def verifica_conexion_ora():

    ruta_ora = os.environ("DB_ORA_URL")
    puerto = os.environ("DB_ORA_PORT")