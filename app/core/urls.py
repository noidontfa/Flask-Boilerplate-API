from flask import Blueprint

from app.core import views
from app.core.api import CoreAPI

core_bp = Blueprint("core", __name__, url_prefix="")
core_api = CoreAPI(core_bp)

core_api.add_resource(views.TokenResource, "/token/")
core_api.add_resource(views.RefreshTokenResource, "/token/refresh/")
core_api.add_resource(views.UserProfileResource, "/profile/")
core_api.add_resource(views.RegisterUserResource, "/register/")
core_api.add_resource(views.VerifyUserResource, "/register/verify/")
core_api.add_resource(views.ResendVerifyUserEmailResource, "/register/resend/")
core_api.add_resource(views.SendResetPasswordResource, "/password/reset/")
core_api.add_resource(views.ResetPasswordResource, "/password/reset/confirm/")
