from werkzeug.exceptions import HTTPException


class GenericException(HTTPException):
    code = 200
    status_code = 500
    description = "Something wrong!"


class TestException(GenericException):
    status_code = 1001
