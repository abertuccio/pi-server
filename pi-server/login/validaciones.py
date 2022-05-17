from errores.errores import Error
import re

# TODO: faltan completar validaciones

def vApp(app):
    app = app.upper()
    return(app)

def vHash(hash):
    return(hash)

def vIp(ip):
    return ip

def vUserAgent(userAgent):
    return userAgent

def vCodigo2fa(codigo):
    return(codigo)

def vUsuarioOrganismo(usuarioOrganismo):
    usuarioOrganismo = usuarioOrganismo.upper()
    if not re.match(r"^[A-ZÑ0-9\_\-]{4,20}$", usuarioOrganismo):
        raise Error('El parametro "usuarioOrganismo" tiene un formato no admitido')
    return(usuarioOrganismo)

def vOrganismo(organismo):
    organismo = organismo.upper()
    if not re.match(r"^[A-ZÑ0-9\_\-\:\.\=]{4,20}$", organismo):
        raise Error('El parametro "organismo" tiene un formato no admitido')
    return(organismo)

def vPassword(password):
    if not re.match(r"^[a-zñA-ZÑ0-9\_\@\-\:\,\.]{8,16}$", password):
        raise Error('El parametro "password" tiene un formato no admitido')
    return(password)