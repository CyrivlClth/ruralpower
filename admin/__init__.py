from flask import Blueprint
from werkzeug.security import generate_password_hash

from admin.auth.views import LoginView, ChangePassword
from common.database import MONGODB, get_uuid
from .merchant_info.views import DataView as MchInfoView
from .product.views import DataView as ProductView, DetailView as ProductDetailView

init_admin = {
    '_id': get_uuid(),
    'username': 'admin',
    'password': generate_password_hash('admin'),
    'type': 'super'
}
MONGODB.get_db('admin_user').update_one({'username': 'admin'}, {'$setOnInsert': init_admin}, upsert=True)

bp = Blueprint('admin', __name__)

bp.add_url_rule('/auth/login', view_func=LoginView.as_view('login'))
bp.add_url_rule('/auth/change_pwd', view_func=ChangePassword.as_view('change_pwd'))

bp.add_url_rule('/mch_info', view_func=MchInfoView.as_view('mch_info'))
bp.add_url_rule('/products', view_func=ProductView.as_view('products'))
bp.add_url_rule('/products/<_id>', view_func=ProductDetailView.as_view('product_detail'))
