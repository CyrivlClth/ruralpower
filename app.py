from flask import Flask

import bill


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bill.bp, url_prefix='/bill')

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
