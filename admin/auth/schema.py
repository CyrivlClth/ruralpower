from flask import request
from marshmallow import Schema, fields
from werkzeug.exceptions import abort


class LoginParam(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @classmethod
    def get_param(cls):
        data = request.get_json()
        if data is None:
            abort(403)
        return cls().load(data)
