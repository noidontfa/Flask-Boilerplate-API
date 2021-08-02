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
SWAGGER_URL = os.environ.get("SWAGGER_URL", "/api/docs")
SWAGGER_API_URL = os.environ.get("SWAGGER_API_URL", "/v1/static/swagger.yaml")
