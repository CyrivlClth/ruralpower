from flask import request
from marshmallow import INCLUDE

from admin.merchant_info.schema import DataSchema
from admin.util.context import get_current_user
from common.database import MONGODB, get_uuid
from common.views import MethodView


class DataView(MethodView):
    col_name = 'merchant'

    def get(self):
        query = dict(_id=get_current_user().mch_id)
        data = MONGODB.get_db(self.col_name).find_one(query)
        assert data
        return DataSchema().load(data, unknown=INCLUDE)

    def post(self):
        data = request.get_json()
        assert data
        data['_id'] = get_uuid()
        info = DataSchema().load(data, unknown=INCLUDE)
        return dict(result=str(MONGODB.get_db(self.col_name).insert_one(info).inserted_id))

    def put(self):
        query = dict(_id=get_current_user().mch_id)
        data = request.get_json()
        assert data
        info = DataSchema(exclude=('_id',), partial=True).load(data, unknown=INCLUDE)
        return dict(result=str(MONGODB.get_db(self.col_name).update_one(query, {'$set': info}).acknowledged))
