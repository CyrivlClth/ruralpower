from flask import Blueprint
from .product import Product, ProductCategory

front = Blueprint('front', __name__, url_prefix='/api')

front.add_url_rule('/products', view_func=Product.as_view('product'))
front.add_url_rule('/products/<id>', view_func=Product.as_view('product_detail'))
front.add_url_rule('/category', view_func=ProductCategory.as_view('category'))
front.add_url_rule('/category/<id>', view_func=ProductCategory.as_view('category_detail'))
