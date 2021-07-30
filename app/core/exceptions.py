from werkzeug.exceptions import HTTPException


class GenericException(HTTPException):
    code = 200
    status_code = 500
    description = "Something wrong!"


class TestException(GenericException):
    status_code = 1001


class NotAuthenticateException(GenericException):
    status_code = 401
    description = "Who Are You?"
