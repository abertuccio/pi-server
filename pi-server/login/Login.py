from login.validaciones import vUsuarioOrganismo, vOrganismo, vPassword, vIp, vUserAgent
from errores.errores import *
from conf.ora_conf import db_ora_conn
from datetime import datetime
import json
import pyotp


class Login:

    esquema_tabla_usuarios = None
    tablas_posibles = ["SEWS.USUARIO",
                       "SEWS.USUARIO_ADMIN", "SEWS.USUARIO_SIBOT"]
    parametros_minimos = ["organismo", "usuarioOrganismo", "password","ip","user-agent"]
    intentos = 0
    datos_usuario_no_validado = None
    datos_usuario_validado = None
    parametros = None
    conn = None
    cursor = None
    meses_desde_ultimo_login = 0

    def __init__(self, parametros={}, esquema_tabla_usuarios=None):

        self.esquema_tabla_usuarios = esquema_tabla_usuarios

        # Verificamos campos mínimos
        key_parametros_list = list(parametros.keys())
        if not all(x in key_parametros_list for x in self.parametros_minimos) or not self.esquema_tabla_usuarios:
            raise Error(
                'No se enviaron los parámetros mínimos de autenticación.')

        # Validamoms todos los campos minimos        
        parametros['usuarioOrganismo'] = vUsuarioOrganismo(
            parametros['usuarioOrganismo'])
        parametros['organismo'] = vOrganismo(parametros['organismo'])
        parametros['password'] = vPassword(parametros['password'])
        parametros['ip'] = vIp(parametros['password'])
        parametros['user-agent'] = vUserAgent(parametros['user-agent'])

        # Si todo el input es correcto abrimos conexión
        self.parametros = parametros
        self.conn = db_ora_conn()
        self.cursor = self.conn.cursor()

        # Existe la combinacion organismo/usuario?
        self.verificacion_existe_organismo_usuario()
    
        # Existe penalización?
        self.verificacion_intentos_penalizacion()

        # Existe la combinacion organismo/usuario/password
        self.verificacion_existe_organismo_usuario_password()

    def verificacion_existe_organismo_usuario(self):

        parametros_identificacion_usuario = {"usuarioOrganismo": self.parametros["usuarioOrganismo"],
                                             "organismo": self.parametros["organismo"]}

        # Independientemente de la tabla de usuarios, el organismo debe estar en la tabla ORGANISMO
        # La tabla de usuarios debe tener el ID_ORGANISMO correspondiente a la tabla ORGANISMO
        q_identificacion_usuarios = """SELECT JSON_OBJECT(o.ID_ORGANISMO , u.*) 
                                    FROM """+self.esquema_tabla_usuarios+""" u
                                    INNER JOIN ORGANISMO o ON u.ID_ORGANISMO = o.ID_ORGANISMO 
                                    WHERE o.USUARIO  = :organismo
                                    AND u.USUARIO = :usuarioOrganismo"""

        self.cursor.execute(q_identificacion_usuarios,
                            parametros_identificacion_usuario)

        datos_usuario = self.cursor.fetchone()

        if not datos_usuario:
            # La combinación de organismo y usuario no existe
            # TODO: Guardar IP y la cantidad de intentos desde la misma
            self.cursor.close()
            self.conn.close()
            raise Error(
                'La combinacion de organismo y usuarioOrganismo no existe')

        self.datos_usuario_no_validado = json.loads(datos_usuario[0])

    def verificacion_existe_organismo_usuario_password(self):

        parametros_identificacion_usuario = {"usuarioOrganismo": self.parametros["usuarioOrganismo"],
                                             "organismo": self.parametros["organismo"], "password": self.parametros["password"]}

        q_password = """SELECT JSON_OBJECT(o.ID_ORGANISMO , u.*) 
                        FROM """+self.esquema_tabla_usuarios+""" u
                        INNER JOIN ORGANISMO o ON u.ID_ORGANISMO = o.ID_ORGANISMO 
                        WHERE o.USUARIO  = :organismo
                        AND u.USUARIO = :usuarioOrganismo AND u.PASSWORD = LOWER(rawtohex(standard_hash(u.RANDOM||:password,'SHA256')))"""

        self.cursor.execute(q_password, parametros_identificacion_usuario)

        datos_usuario_validado = self.cursor.fetchone()

        if not datos_usuario_validado:
            # El password es incorrecto
            # TODO: Penalizar
            self.penalizacion()
            self.cursor.close()
            self.conn.close()
            raise Error('El password es incorrecto')

        self.datos_usuario_validado = json.loads(datos_usuario_validado[0])

    def verificacion_intentos_penalizacion(self):

        parametros_penalizacion = {
            "usuario": self.datos_usuario_no_validado["USUARIO"], "id_organismo": self.datos_usuario_no_validado["ID_ORGANISMO"]}

        q_penalizacion = """SELECT (ULTIMO_INTENTO  + (POWER(3,INTENTOS)/(24*60*60))*INTENTOS) PROXIMO_INTENTO
                            FROM """+self.esquema_tabla_usuarios+""" u
                            WHERE UPPER(USUARIO) = UPPER(:usuario)
                            AND ID_ORGANISMO = :id_organismo"""

        self.cursor.execute(q_penalizacion, parametros_penalizacion)

        fecha_hasta_penalizacion = self.cursor.fetchone()

        fecha_hasta_penalizacion = fecha_hasta_penalizacion[0]

        if not fecha_hasta_penalizacion:
            return

        ahora = datetime.now()

        if fecha_hasta_penalizacion > ahora:
            raise Error(
                'El usuario se encuentra penalizado hasta el ' + fecha_hasta_penalizacion.strftime('%d-%m-%Y %H:%M:%S'))

    def penalizacion(self):

        self.intentos = 1 if not self.datos_usuario_no_validado[
            "INTENTOS"] else self.datos_usuario_no_validado["INTENTOS"] + 1

        parametros_penalizacion = {
            "id_usuario": self.datos_usuario_no_validado["ID_USUARIO"], "intentos": self.intentos}

        q_penalizacion = """UPDATE """+self.esquema_tabla_usuarios+""" 
                            SET INTENTOS = :intentos, 
                            ULTIMO_INTENTO = SYSDATE 
                            WHERE ID_USUARIO = :id_usuario"""

        self.cursor.execute(q_penalizacion,
                            parametros_penalizacion)

        self.conn.commit()
