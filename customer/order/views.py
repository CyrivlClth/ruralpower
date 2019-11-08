from flask import jsonify, request
from marshmallow import INCLUDE, EXCLUDE
from werkzeug.exceptions import abort

from common.auth import login_required
from common.database import MONGODB
from common.views import MethodView, page_param
from customer.order.schema import DataSchema, QuerySchema


class DataView(MethodView):
    decorators = (login_required,)
    col_name = 'product'

    def get(self):
        query = QuerySchema().load(request.args)
        print(dir(request.headers))
        pager = page_param()
        data = MONGODB.get_db(self.col_name).find(query, skip=pager.skip, limit=pager.limit)
        assert data
        return jsonify(DataSchema(many=True).load(data, unknown=EXCLUDE))


class DetailView(MethodView):
    col_name = 'product'

    def get(self, _id):
        query = QuerySchema().load(request.args)
        print(query)
        data = MONGODB.get_db(self.col_name).find_one(query)
        if not data:
            abort(404)
        return DataSchema().load(data, unknown=INCLUDE)
