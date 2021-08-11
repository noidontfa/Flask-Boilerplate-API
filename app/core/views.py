from flask import request

from app.core.resources import AllowAnyResource, AuthenticationResource
from app.core.schemas import (
    LoginSchema,
    RegisterSchema,
    ResendEmailSchema,
    ResetPasswordSchema,
    SendResetPasswordSchema,
    UserSchema,
    VerificationSchema,
)
from app.core.services import CoreService


class TokenResource(AllowAnyResource):
    def post(self, *args, **kwargs):
        data = request.get_json(force=True)
        login_schema = LoginSchema()
        user = login_schema.load(data)
        result = CoreService.generate_user_token(user_id=user.id)
        return result, 200


class RefreshTokenResource(AllowAnyResource):
    def get(self, *args, **kwargs):
        user_id = CoreService.get_user_identity(refresh=True)
        result = CoreService.generate_user_token(user_id=user_id)
        return result, 200


class UserProfileResource(AuthenticationResource):
    def get(self, *args, **kwargs):
        user = request.user
        user_schema = UserSchema()
        result = user_schema.dump(user)
        return result, 200


class RegisterUserResource(AllowAnyResource):
    def post(self, *args, **kwargs):
        data = request.get_json(force=True)
        user = RegisterSchema().load(data)
        return UserSchema().dump(user), 201


class VerifyUserResource(AllowAnyResource):
    def post(self, *args, **kwargs):
        data = request.get_json(force=True)
        token = VerificationSchema().load(data)
        return token, 200


class ResendVerifyUserEmailResource(AllowAnyResource):
    def post(self, *args, **kwargs):
        data = request.get_json(force=True)
        ResendEmailSchema().load(data)
        return "Sent", 200


class SendResetPasswordResource(AllowAnyResource):
    def post(self, *args, **kwargs):
        data = request.get_json(force=True)
        SendResetPasswordSchema().load(data)
        return "Sent", 200


class ResetPasswordResource(AllowAnyResource):
    def post(self, *args, **kwargs):
        data = request.get_json(force=True)
        ResetPasswordSchema().load(data)
        return "Reset Successfully", 200
