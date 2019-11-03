from flask import Blueprint
from .product import Product, ProductCategory

admin = Blueprint('admin', __name__, url_prefix='/admin')

admin.add_url_rule('/products', view_func=Product.as_view('product'))
admin.add_url_rule('/products/<id>', view_func=Product.as_view('product_detail'))
admin.add_url_rule('/category', view_func=ProductCategory.as_view('category'))
admin.add_url_rule('/category/<id>', view_func=ProductCategory.as_view('category_detail'))
