from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from app.core.models import User
from app.core.utils import send_mail


class CoreService:
    @classmethod
    def generate_user_token(cls, user_id):
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return dict(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    def get_user_identity(cls, refresh=False):
        @jwt_required(refresh=refresh)
        def identify():
            return get_jwt_identity()

        user_id = identify()
        return user_id

    @classmethod
    def send_register_email(cls, user: User):
        subject = "Register"
        template_name = "user/register.html"
        context = dict(key=user.email_address.key, username=user.name)
        send_mail(subject, template_name, context, user.email)

    @classmethod
    def send_reset_password(cls, user: User):
        subject = "Reset Password"
        template_name = "user/reset_password.html"
        context = dict(key=user.reset_password.key, username=user.name)
        send_mail(subject, template_name, context, user.email)
