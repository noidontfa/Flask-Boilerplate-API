from flask import Blueprint, Flask

from app.extensions import db, jwt, ma, migrate


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def create_app(config="settings.py"):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile(config)
    from app.urls import initial_blueprint

    register_extensions(app)
    v1_bp = Blueprint("v1", __name__, url_prefix="/v1")
    initial_blueprint(v1_bp)
    app.register_blueprint(v1_bp)

    return app


app = create_app()
