from marshmallow import post_load, validate

from app.core.exceptions import (
    LoginException,
    ResendEmailException,
    ValidationException,
    VerificationException,
)
from app.core.models import EmailAddress, User
from app.core.services import CoreService
from app.core.validators import CheckEmailExist, CheckNoneEmail
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
        if not user.is_email_verified:
            raise LoginException(description="User is not verified")
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
        email_address = EmailAddress(email=data.get("email"))
        email_address.generate_key()
        user = User(**data, email_address=email_address)
        user.set_password(password1)
        user.save()
        CoreService.send_register_email(user)
        return user


class VerificationSchema(ma.Schema):
    email = ma.Email(required=True, allow_none=False, validate=[CheckNoneEmail()])
    key = ma.Str(required=True, allow_none=False)

    @post_load
    def load_instance(self, data, *args, **kwargs):
        email = data.get("email")
        key = data.get("key")
        email_address = EmailAddress.query.filter_by(email=email).first()
        user = email_address.confirm(key=key)
        if not user:
            raise VerificationException()
        return CoreService.generate_user_token(user.id)


class ResendEmailSchema(ma.Schema):
    email = ma.Email(required=True, allow_none=False, validate=[CheckNoneEmail()])

    @post_load
    def load_instance(self, data, *args, **kwargs):
        email = data.get("email")
        user = User.query.filter_by(email=email).first()
        if user.is_email_verified:
            raise ResendEmailException()
        user.email_address.generate_key()
        CoreService.send_register_email(user.save())
