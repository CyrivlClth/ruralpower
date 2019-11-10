from flask import request
from flask.views import MethodView as BaseView, View
from itsdangerous import TimedJSONWebSignatureSerializer
from marshmallow import Schema
from pymongo.collection import Collection
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash

from common.database import MONGODB, get_uuid
from common.schema import Pager, PageSchema, BaseSchema, LoginParam


def page_param() -> Pager:
    return PageSchema().load(request.args)


class MethodView(BaseView):  # type:View
    pass


class DataView(MethodView):  # type:View
    col_name: str
    db_name: str = None
    detail_schema: Schema
    list_schema: Schema
    create_schema: Schema
    update_schema: Schema

    def object_permission(self, query: dict):
        return query

    def get(self, _id=None):
        if _id is None:
            return self.list()
        data = self.collection().find_one(self.object_permission({'_id': _id}))
        if not data:
            abort(404)
        return self.detail_schema.load(data)

    def list(self):
        return self.list_schema.load(self.collection().find(self.object_permission(dict())))

    def collection(self) -> Collection:
        return MONGODB.get_db(self.col_name, self.db_name)

    def put(self, _id):
        json = request.get_json()
        data = self.update_schema.load(json)
        if self.collection().update_one(self.object_permission({'_id': _id}), {'$set': data}).acknowledged:
            return data
        abort(403)

    def post(self):
        json = request.get_json()
        data = self.create_schema.load(json)
        data = self.object_permission(data)
        data['_id'] = get_uuid()
        if self.collection().insert_one(data).acknowledged:
            return data
        abort(403)


class LoginView(MethodView):
    col_name: str
    platform: str
    signer: TimedJSONWebSignatureSerializer
    db_name: str = None
    schema: BaseSchema = LoginParam

    def __init__(self, col_name, signer, platform, db_name=None, schema=None):
        self.col_name = col_name
        self.signer = signer
        self.platform = platform
        if db_name is not None:
            self.db_name = db_name
        if schema is not None:
            self.schema = schema

    def post(self):
        user = self.schema.get_param()
        query = dict(username=user['username'])
        obj = MONGODB.get_db(self.col_name, self.db_name).find_one(query)
        assert obj
        assert check_password_hash(obj.get('password'), user['password'])
        data = {'platform': self.platform, 'username': user['username'], 'user_id': obj['_id']}
        result = dict(token=self.signer.dumps(data).decode())
        return result
