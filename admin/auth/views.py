import time

from werkzeug.security import check_password_hash, generate_password_hash

from admin.auth.schema import LoginParam, ChangePasswordParam
from admin.util.context import get_current_user
from common.auth import signer
from common.database import MONGODB
from common.errors import HandlerException
from common.views import MethodView


class LoginView(MethodView):
    col_name = 'admin_user'

    def post(self):
        user = LoginParam.get_param()
        query = dict(username=user['username'])
        obj = MONGODB.get_db(self.col_name).find_one(query)
        assert obj
        assert check_password_hash(obj.get('password'), user['password'])
        data = {'username': user['username'], 'user_id': obj['_id']}
        result = dict(token=signer.dumps(data).decode())
        print(time.time())
        return result


class ChangePassword(MethodView):
    col_name = 'admin_user'

    def post(self):
        pwd = ChangePasswordParam.get_param()
        user_id = get_current_user().get_id()
        user = MONGODB.get_db(self.col_name).find_one({'_id': user_id}, {'password': 1})
        if not user:
            raise HandlerException(status_code=500, message='unknown error')
        if not check_password_hash(user['password'], pwd.get('old_password')):
            raise HandlerException(status_code=403, message='error old password')
        result = MONGODB.get_db(self.col_name).update_one({'_id': user_id}, {
            '$set': {'password': generate_password_hash(pwd['new_password'])}})
        if result.modified_count != 1:
            raise HandlerException(status_code=403,message='change password failed')
        return 'ok'
