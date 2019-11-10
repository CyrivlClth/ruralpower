from flask import request
from marshmallow import Schema, fields, post_load, EXCLUDE
from werkzeug.exceptions import abort


class Pager(object):
    page: int
    page_size: int

    def __init__(self, page=1, page_size=10, **kwargs):
        self.page = page
        self.page_size = page_size

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PageSchema(Schema):
    page = fields.Integer(default=1)
    page_size = fields.Integer(default=10)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_this(self, data, **kwargs):
        return Pager(**data)


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
