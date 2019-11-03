from flask import Flask
from ruralpower.common.views import JSONResponse

app = Flask(__name__)
app.response_class = JSONResponse

from ruralpower.views.admin import admin

app.register_blueprint(admin)

from ruralpower.views.front import front

app.register_blueprint(front)

if __name__ == '__main__':
    app.run(debug=True)
