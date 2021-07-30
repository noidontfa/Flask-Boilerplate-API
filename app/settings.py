import os

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
