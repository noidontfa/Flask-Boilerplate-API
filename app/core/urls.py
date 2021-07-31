from flask import Blueprint

from app.core import views
from app.core.api import CoreAPI

core_bp = Blueprint("core", __name__, url_prefix="")
core_api = CoreAPI(core_bp)

core_api.add_resource(views.TokenResource, "/token/")
core_api.add_resource(views.RefreshTokenResource, "/token/refresh/")
core_api.add_resource(views.UserProfileResource, "/profile")
