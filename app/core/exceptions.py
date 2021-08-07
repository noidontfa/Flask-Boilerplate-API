from werkzeug.exceptions import HTTPException


class GenericException(HTTPException):
    code = 200
    status_code = 500
    description = "Something wrong!"


class ValidationException(GenericException):
    status_code = 1000


class LoginException(GenericException):
    status_code = 401
    description = "Unable to log in with provided credentials."


class VerificationException(GenericException):
    status_code = 400
    description = "Unable to verify with provided credentials."


class ResendEmailException(GenericException):
    status_code = 400
    description = "User is verified"
