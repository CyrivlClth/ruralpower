from pymongo import MongoClient
from pymongo.collection import ObjectId
from flask import request, jsonify
from ruralpower.common.views import MethodView


class Product(MethodView):
    db = MongoClient('localhost')
    table_name = 'products'

    def get(self, id=None):
        if id is not None:
            data = self.get_db().find_one({'_id': ObjectId(id)})
            data['_id'] = str(data['_id'])
            return jsonify(data)
        data = list()
        for i in self.get_db().find({}):
            i['_id'] = str(i['_id'])
            data.append(i)
        return jsonify(data)


class ProductCategory(Product):
    table_name = 'product_category'
