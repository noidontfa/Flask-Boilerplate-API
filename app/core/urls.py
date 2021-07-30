from flask import Blueprint
from flask_restful import Api

from app.core.api import CoreAPI
from app.core.views import TestResource

core_bp = Blueprint("core", __name__, url_prefix="")
core_api = CoreAPI(core_bp)

core_api.add_resource(TestResource, "/")
