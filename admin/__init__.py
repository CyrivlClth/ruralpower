from flask import Flask

from admin.merchant_info.views import DataView
from admin.admin_user.views import DataView as AdminUserView
from admin.product.views import DataView as ProductView,DetailView

app = Flask(__name__)
app.add_url_rule('/', view_func=DataView.as_view('mch_info'))
app.add_url_rule('/admin_users', view_func=AdminUserView.as_view('admin_users'))
app.add_url_rule('/products', view_func=ProductView.as_view('products'))
app.add_url_rule('/products/<_id>', view_func=DetailView.as_view('product_detail'))

if __name__ == '__main__':
    app.run(debug=True)
