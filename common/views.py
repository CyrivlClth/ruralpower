from flask import request
from flask.views import MethodView

from common.schema import Pager, PageSchema


def page_param() -> Pager:
    return PageSchema().load(request.args)
