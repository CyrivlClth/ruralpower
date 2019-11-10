from flask import request
from marshmallow import Schema, fields
from werkzeug.exceptions import abort


class BaseSchema(Schema):
    @classmethod
    def get_param(cls):
        data = request.get_json()
        if data is None:
            abort(403)
        return cls().load(data)


class LoginParam(BaseSchema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class ChangePasswordParam(BaseSchema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
