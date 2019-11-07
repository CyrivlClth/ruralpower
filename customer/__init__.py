from flask import Flask

from customer.auth.views import RegisterView, LoginView
from customer.product.views import DataView

app = Flask(__name__)

app.add_url_rule('/', view_func=DataView.as_view('product'))
app.add_url_rule('/register', view_func=RegisterView.as_view('register'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))

if __name__ == '__main__':
    app.run(debug=True)
