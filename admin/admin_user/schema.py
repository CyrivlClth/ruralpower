from marshmallow import Schema, fields


class DataSchema(Schema):
    _id = fields.String(required=True)
    name = fields.String(required=True)
    mch_id = fields.String(required=True)
    mch_name = fields.String(required=True)
