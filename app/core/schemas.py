from marshmallow import post_load, validate

from app.core.exceptions import LoginException, ValidationException
from app.core.models import User
from app.core.validators import CheckEmailExist
from app.extensions import ma


class LoginSchema(ma.Schema):
    email = ma.Email(required=True, allow_none=False)
    password = ma.Str(required=True, allow_none=False)

    @post_load
    def load_user(self, data, *args, **kwargs):
        email = data.get("email")
        password = data.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise LoginException()
        return user


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password",)


class RegisterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ["id", "name", "email", "password1", "password2"]

    email = ma.Email(required=True, validate=[CheckEmailExist()])
    password1 = ma.Str(
        required=True, load_only=True, validate=[validate.Length(min=8, max=16)]
    )
    password2 = ma.Str(
        required=True, load_only=True, validate=[validate.Length(min=8, max=16)]
    )

    @post_load
    def load_user(self, data, *args, **kwargs):
        password1 = data.pop("password1")
        password2 = data.pop("password2")
        if password1 != password2:
            raise ValidationException(description="Password does not match")
        user = User(**data)
        user.set_password(password1)
        return user
