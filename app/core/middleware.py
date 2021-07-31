import traceback
from functools import wraps

from flask import request
from marshmallow import ValidationError

from app.core.exceptions import GenericException, ValidationException
from app.core.models import User
from app.core.services import CoreService


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = CoreService.get_user_identity()
        request.user = User.query.get(user_id)
        return func(*args, **kwargs)

    return wrapper


def wrap_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            traceback.print_exc()
            raise ValidationException(description=e.messages)
        except GenericException as e:
            traceback.print_exc()
            raise e
        except Exception:
            traceback.print_exc()
            raise GenericException()

    return wrapper
