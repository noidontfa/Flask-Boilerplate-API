from flask import Blueprint
from flask_restful import Api

from app.core.views import TestResource

core_bp = Blueprint("core", __name__, url_prefix="")
core_api = Api(core_bp)

core_api.add_resource(TestResource, "/")
