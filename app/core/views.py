from flask import request

from app.core.exceptions import LoginException
from app.core.models import User
from app.core.resources import AllowAnyResource, AuthenticationResource
from app.core.schemas import LoginSchema, UserSchema
from app.core.services import CoreService


class TokenResource(AllowAnyResource):
    def post(self, *args, **kwargs):
        data = request.get_json()
        login_schema = LoginSchema()
        schema_data = login_schema.load(data)

        user = User.query.filter_by(**schema_data).first()
        if not user:
            raise LoginException()
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
