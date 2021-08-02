from flask import request

from app.core.resources import AllowAnyResource, AuthenticationResource
from app.core.schemas import LoginSchema, RegisterSchema, UserSchema
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
        user.save()
        return UserSchema().dump(user), 201
