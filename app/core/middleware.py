import traceback
from functools import wraps

from app.core.exceptions import GenericException, NotAuthenticateException


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        raise NotAuthenticateException()
        # return func(*args, **kwargs)

    return wrapper


def wrap_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GenericException as e:
            traceback.print_exc()
            raise e
        except Exception:
            traceback.print_exc()
            raise GenericException()

    return wrapper
