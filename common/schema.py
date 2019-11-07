from dataclasses import dataclass

from marshmallow import Schema, fields, post_load


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

    @post_load
    def make_this(self, data, **kwargs):
        return Pager(**data)
