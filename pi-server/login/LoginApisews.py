from login.Login import Login
from errores.errores import *
import os
import hashlib
import time

# Clase que extiente Login
class LoginApisews(Login):

    limite_consultas = 0
    token = None
    minutos_validez_token_defecto = int(os.environ.get('MINUTOS_VALIDEZ_TOKEN_DEFECTO')) if os.environ.get('MINUTOS_VALIDEZ_TOKEN_DEFECTO') else 20
    segundos_validez_token = 0    

    def __init__(self, parametros={}):

        super().__init__(parametros,"SEWS.USUARIO")

        self.verificacion_usuario_bloqueado_eliminado()
        self.verificacion_limite_consultas()
        self.generarToken()

    def verificacion_usuario_bloqueado_eliminado(self):

        if self.datos_usuario_validado["BORRADO"] == "E":
            raise Error('El usuario fue eliminado.')

        if self.datos_usuario_validado["BORRADO"] == "SI":
            raise Error('El usuario está bloqueado.')

        if self.datos_usuario_validado["BORRADO"] != "NO":
            raise Error('El usuario no está habilitado para realizar consultas.')

        return    

    def verificacion_limite_consultas(self):

        parametros_bloqueo = {"organismo":self.parametros["organismo"]}

        q_limite_consultas = """SELECT (LIMITE_MENSUAL - CONSULTAS_MENSUALES) LIMITE_CONSULTAS, 
        BLOQUEADO, 
        ID_ORGANISMO 
        FROM ORGANISMO 
        WHERE UPPER(USUARIO) = UPPER(:organismo)"""

        self.cursor.execute(q_limite_consultas,
                    parametros_bloqueo)

        res = self.cursor.fetchone()

        if not res:
            raise Error('Hubo un error inesperado.')

        self.limite_consultas = res[0]

        if self.limite_consultas < 1:
            raise Error('El organismo alcanzó el límite de consultas mensuales habilitadas.')

        return

    def generarToken(self):

        mt = str(round(time.time() * 1000))

        random = str(os.urandom(44).hex())

        self.token = hashlib.sha512( str( mt +  random).encode("utf-8") ).hexdigest()

        self.segundos_validez_token = int(time.time()) + (self.minutos_validez_token_defecto * 60)