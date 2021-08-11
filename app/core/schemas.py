from marshmallow import ValidationError, post_load, validate, validates

from app.core.exceptions import (
    LoginException,
    ResendEmailException,
    UserNotExistException,
    UserNotFoundException,
    ValidationException,
    VerificationException,
)
from app.core.models import EmailAddress, ResetPassword, User
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

    @validates("email")
    def validate_email(self, email):
        email_address = EmailAddress.query.filter_by(email=email).first()
        if not email_address:
            raise ValidationError("Email is not found or already verified")
        return email

    @post_load
    def load_instance(self, data, *args, **kwargs):
        email = data.get("email")
        key = data.get("key")
        email_address = EmailAddress.query.filter_by(email=email).first()
        user = email_address.confirm(key=key)
        if not user:
            raise VerificationException()
        email_address.delete()
        return CoreService.generate_user_token(user.id)


class ResendEmailSchema(ma.Schema):
    email = ma.Email(required=True, allow_none=False, validate=[CheckNoneEmail()])

    @validates("email")
    def validate_email(self, email):
        email_address = EmailAddress.query.filter_by(email=email).first()
        if not email_address:
            raise ValidationError("Email is not exist")
        return email

    @post_load
    def load_instance(self, data, *args, **kwargs):
        email = data.get("email")
        user = User.query.filter_by(email=email).first()
        if user.is_email_verified:
            raise ResendEmailException()
        if user.email_address:
            email_address = user.email_address
            email_address.delete()
        email_address = EmailAddress(email=email)
        email_address.generate_key()
        user.email_address = email_address
        user.commit()

        user.email_address.generate_key()
        CoreService.send_register_email(user)


class SendResetPasswordSchema(ma.Schema):
    email = ma.Str(required=True, allow_none=False, validate=[CheckNoneEmail()])

    @validates("email")
    def validate_email(self, email):
        user = User.query.filter(User.email == email).first()
        if not user:
            raise UserNotExistException()
        return email

    @post_load
    def load_instance(self, data, *args, **kwargs):
        email = data.get("email")
        user = User.query.filter(User.email == email).first()
        if user.reset_password:
            reset_password = user.reset_password
            reset_password.delete()
        reset_password = ResetPassword()
        reset_password.generate_key()
        user.reset_password = reset_password
        user.commit()
        CoreService.send_reset_password(user.save())


class ResetPasswordSchema(ma.Schema):
    key = ma.Str(required=True, allow_none=False)
    email = ma.Str(required=True, validate=[CheckNoneEmail()])
    new_password1 = ma.Str(
        required=True, load_only=True, validate=[validate.Length(min=8, max=16)]
    )
    new_password2 = ma.Str(
        required=True, load_only=True, validate=[validate.Length(min=8, max=16)]
    )

    @post_load
    def load_instance(self, data, *args, **kwargs):
        email = data.get("email")
        key = data.get("key")
        new_password1 = data.get("new_password1")
        new_password2 = data.get("new_password2")
        if new_password1 != new_password2:
            raise ValidationException(description="Password does not match")
        reset_password = (
            ResetPassword.query.join(User)
            .filter(User.email == email, ResetPassword.key == key)
            .first()
        )
        if not reset_password:
            raise UserNotFoundException()
        flag = reset_password.set_new_password(key, new_password1)
        if not flag:
            raise ValidationException(
                description="Can not reset password with provided key"
            )
        reset_password.delete()
