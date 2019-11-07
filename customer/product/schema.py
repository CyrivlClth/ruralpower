from marshmallow import Schema, fields, EXCLUDE


class DataSchema(Schema):
    _id = fields.String(required=True)
    name = fields.String(required=True)


class QuerySchema(Schema):
    class Meta:
        additional = ('mch_id',)
        unknown = EXCLUDE
