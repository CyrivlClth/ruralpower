from pymongo import MongoClient
from pymongo.collection import ObjectId
from flask import request, jsonify
from ruralpower.common.views import MethodView


class Product(MethodView):
    db = MongoClient('localhost')
    table_name = 'products'

    def get(self, id=None):
        mch_id = '1'
        if id is None:
            data = list()
            for i in self.get_db().find({'mch_id': mch_id}):
                i['_id'] = str(i['_id'])
                data.append(i)
            return jsonify(data)

        data = self.get_db().find_one({'_id': ObjectId(id), 'mch_id': mch_id})
        data['_id'] = str(data['_id'])
        return jsonify(data)

    def post(self):
        data = request.get_json()
        mch_id = '1'
        data['mch_id'] = mch_id
        return str(self.get_db().insert_one(data).inserted_id)

    def delete(self, id):
        mch_id = '1'
        query = {'_id': ObjectId(id), 'mch_id': mch_id}
        return str(self.get_db().delete_one(query).deleted_count)

    def put(self, id):
        mch_id = '1'
        data = request.get_json()
        data['mch_id'] = mch_id
        data.pop('_id', None)
        return str(self.get_db().update_one({'_id': ObjectId(id), 'mch_id': mch_id}, {'$set': data}).modified_count)


class ProductCategory(Product):
    table_name = 'product_category'
