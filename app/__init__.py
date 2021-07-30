from flask import Blueprint, Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def create_app(config="settings.py"):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile(config)
    from app.urls import initial_blueprint

    v1_bp = Blueprint("v1", __name__, url_prefix="/v1")
    initial_blueprint(v1_bp)
    app.register_blueprint(v1_bp)

    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
