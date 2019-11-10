from flask import Blueprint
from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash

from common.database import get_uuid, MONGODB
from common.views import LoginView


class BillConfig:
    platform = 'bill'
    db_name = 'rural_bill'
    user_col = 'user'


signer = TimedJSONWebSignatureSerializer('IVxZQ8t6vM9NmbHw7xbtEvCYDWYpW3xR1Aw/1l3LeX7gCGS/2zMa6qXIZC273Q==',
                                         expires_in=60 * 15)

init_admin = {
    '_id': get_uuid(),
    'username': 'admin',
    'password': generate_password_hash('admin'),
    'type': 'super'
}
MONGODB.get_db(BillConfig.user_col, BillConfig.db_name).update_one({'username': 'admin'}, {'$setOnInsert': init_admin},
                                                                   upsert=True)

bp = Blueprint('bill', __name__)

bp.add_url_rule('/auth/login', view_func=LoginView.as_view('login', BillConfig.user_col, signer, BillConfig.platform,
                                                           db_name=BillConfig.db_name))
