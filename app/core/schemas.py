from app.core.models import User
from app.extensions import ma


class LoginSchema(ma.Schema):
    email = ma.Email(required=True, allow_none=False)
    password = ma.Str(required=True, allow_none=False)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        fields = ["id", "name", "email"]
