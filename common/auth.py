from functools import wraps

from flask import request, g
from itsdangerous import TimedJSONWebSignatureSerializer, BadData, SignatureExpired
from werkzeug.exceptions import abort

from config import Config

signer = TimedJSONWebSignatureSerializer(Config.JWT_SECRET, expires_in=Config.JWT_EXPIRED)


def login_required(f):
    @wraps(f)
    def d(*args, **kwargs):
        token = request.headers.get(Config.JWT_HEADER)
        try:
            g.auth_data = signer.loads(token)
            return f(*args, **kwargs)
        except SignatureExpired:
            abort(401)
        except BadData:
            abort(401)

    return d
