from marshmallow.validate import ValidationError, Validator

from app.core.models import User


class CheckEmailExist(Validator):

    default_error = "Email is already existed"

    def __init__(self, error=None):
        self.error = error if error else self.default_error

    def __call__(self, value, *args, **kwargs):
        if User.query.filter_by(email=value).first():
            raise ValidationError(self.error)
        return value
