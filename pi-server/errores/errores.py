from flask import jsonify

class Error(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['status'] = "Error"
        rv['mensaje'] = self.message
        return rv

# Usar únicamente donde no se puede usar raise
def mensaje_error(message, status_code=None, payload=None):
    m = Error(message, status_code=None, payload=None)
    return jsonify(m.to_dict())