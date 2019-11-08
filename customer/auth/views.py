import time

from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from common.auth import signer, login_required
from common.database import MONGODB, get_uuid
from common.views import MethodView
from customer.auth.schema import LoginParam, ChangeParam
from customer.util.context import get_current_user


class LoginView(MethodView):
    col_name = 'users'

    def post(self):
        print(time.time())
        user = LoginParam.get_param()
        query = dict(username=user['username'])
        obj = MONGODB.get_db(self.col_name).find_one(query)
        assert obj
        assert check_password_hash(obj.get('password'), user['password'])
        data = {'username': user['username'], 'user_id': obj['_id']}
        result = dict(token=signer.dumps(data).decode())
        print(time.time())
        return result


class RegisterView(MethodView):
    col_name = 'users'

    def post(self):
        user = LoginParam.get_param()
        user['password'] = generate_password_hash(user.get('password'))
        user['_id'] = get_uuid()
        result = MONGODB.get_db(self.col_name).update_one(dict(username=user.get('username')), {'$setOnInsert': user},
                                                          upsert=True)
        if result.upserted_id is None:
            return '已被注册'
        return jsonify(str(result.upserted_id))


class ChangePasswordView(MethodView):
    col_name = 'users'
    decorators = [login_required]

    def post(self):
        pwd = ChangeParam.get_param()
        query = {'_id': get_current_user().get_id()}
        user = MONGODB.get_db(self.col_name).find_one(query, {'password': 1})
        assert check_password_hash(user['password'], pwd['old_password'])
        result = MONGODB.get_db(self.col_name).update_one(query, {
            '$set': {'password': generate_password_hash(pwd.get('new_password'))}})
        return jsonify(str(result.modified_count))
