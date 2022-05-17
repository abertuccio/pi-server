from login.validaciones import vApp, vHash, vCodigo2fa
from login.LoginApisews import LoginApisews
from errores.errores import *

# Clase que extiente Login > LoginApisews
class LoginEco(LoginApisews):

    parametros_minimos = ["hash", "app"]

    def __init__(self):

        # Verificamos campos mínimos para eco
        key_parametros_list = list(LoginApisews.parametros.keys())
        if not all(x in key_parametros_list for x in self.parametros_minimos) or not self.esquema_tabla_usuarios:
            raise Error(
                'No se enviaron los parámetros mínimos de autenticación para eco.')

        # Validamoms todos los campos especificos para eco
        LoginApisews.parametros['app'] = vApp(
            LoginApisews.parametros['app']) if 'app' in LoginApisews.parametros else None
        LoginApisews.parametros['hash'] = vHash(
            LoginApisews.parametros['hash']) if 'hash' in LoginApisews.parametros else None
        LoginApisews.parametros['codigo_2fa'] = vCodigo2fa(
            LoginApisews.parametros['codigo_2fa']) if 'codigo_2fa' in LoginApisews.parametros else None

        if LoginApisews.meses_desde_ultimo_login >= 2 and not LoginApisews.parametros['codigo_2fa']:
            raise Error('Es necesario que envíe codigo del segundo factor de autenicación')

        # Verificamos que el cliente este habilitado

    def habillitacion_cliente():
        q_habilitacion_cliente = """SELECT COUNT(1) HABILITACION FROM CLIENTE_HABILITADO
                                    WHERE APP = :app
                                    AND HASH = :hash"""

    def verificacion_2fa(self):
        usuarioSecret = "JBSWY3DPEHPK3PXP"
        totp = pyotp.TOTP(usuarioSecret)

        if self.parametros['codigo_2fa'] !=  totp:
            raise Error('El código 2fa es incorrecto.')

        self.codigo_2fa_valido = True
