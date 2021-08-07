import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

APP = "app"
ENV = os.environ.get("ENV")
DEBUG = os.environ.get("DEBUG")
TESTING = os.environ.get("TESTING")
# CSRF_ENABLED = True
SECRET_KEY = "this-really-needs-to-be-changed"
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = True
# JWT_COOKIE_SECURE = os.environ.get("JWT_COOKIE_SECURE", default=False)
JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = timedelta(
    minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 300))
)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(
    minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 300)) * 2
)

# SWAGGER CONFIG
SWAGGER_URL = os.environ.get("SWAGGER_URL", "/api/docs")
SWAGGER_API_URL = os.environ.get("SWAGGER_API_URL", "/v1/static/swagger.yaml")

# MAIL CONFIG
MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
MAIL_PORT = int(os.environ.get("MAIL_PORT", 25))
MAIL_USE_TLS = os.environ.get("MAIL_USER_TLS", False)
MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", False)
MAIL_DEBUG = os.environ.get("MAIL_DEBUG", True)
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", None)
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", None)
MAIL_DEFAULT_SENDER = os.environ.get(
    "MAIL_DEFAULT_SENDER", "Thinh ngo <thinhngo1198@gmail.com>"
)
MAIL_MAX_EMAILS = os.environ.get("MAIL_MAX_EMAILS", None)
MAIL_SUPPRESS_SEND = os.environ.get("MAIL_SUPPRESS_SEND", True)
MAIL_ASCII_ATTACHMENTS = os.environ.get("MAIL_ASCII_ATTACHMENTS", False)
EMAIL_CONFIRMATION_EXPIRE_DAYS = int(
    os.environ.get("EMAIL_CONFIRMATION_EXPIRE_DAYS", 2)
)
