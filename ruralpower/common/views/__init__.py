from flask import Response, jsonify
from flask.views import MethodView as MV
from pymongo import MongoClient
from pymongo.collection import Collection


class MethodView(MV):
    database_name: str = 'ruralpower'
    table_name: str = 'example'
    db: MongoClient = None

    def get_db(self) -> Collection:
        assert self.db is not None
        return self.db.get_database(self.database_name).get_collection(self.table_name)


# 定义response返回类,自动解析json
class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        # if isinstance(response, dict, list, tuple):  # 判断返回类型是否是字典(JSON)
        response = jsonify(response)  # 转换
        return super().force_type(response, environ)
