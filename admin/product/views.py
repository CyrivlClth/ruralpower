from flask import request, jsonify
from marshmallow import INCLUDE
from werkzeug.exceptions import abort

from admin.product.schema import DataSchema
from admin.util.context import get_current_user
from common.database import MONGODB, get_uuid
from common.views import MethodView, page_param


class DataView(MethodView):
    col_name = 'product'

    def get(self):
        query = dict(mch_id=get_current_user().mch_id)
        pager = page_param()
        data = MONGODB.get_db(self.col_name).find(query, skip=pager.skip, limit=pager.limit)
        assert data
        return jsonify(DataSchema(many=True).load(data, unknown=INCLUDE))

    def post(self):
        data = request.get_json()
        assert data
        data['_id'] = get_uuid()
        info = DataSchema().load(data, unknown=INCLUDE)
        return dict(result=str(MONGODB.get_db(self.col_name).insert_one(info).inserted_id))


class DetailView(MethodView):
    col_name = 'product'

    def get(self, _id):
        query = dict(_id=_id, mch_id=get_current_user().mch_id)
        data = MONGODB.get_db(self.col_name).find_one(query)
        if not data:
            abort(404)
        return DataSchema().load(data, unknown=INCLUDE)

    def put(self, _id):
        query = dict(_id=_id, mch_id=get_current_user().mch_id)
        data = request.get_json()
        assert data
        info = DataSchema(exclude=('_id',), partial=True).load(data, unknown=INCLUDE)
        return dict(result=str(MONGODB.get_db(self.col_name).update_one(query, {'$set': info}).acknowledged))
