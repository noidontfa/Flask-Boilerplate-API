from os.path import abspath, dirname, join

from flask import Blueprint, Flask, send_from_directory

from app.extensions import bcrypt, db, jwt, ma, mail, migrate

base_dir = dirname(dirname(abspath(__file__)))
static_path = join(base_dir, "static")


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)


def create_app(config="settings.py"):
    # create and configure the app
    app = Flask(__name__, static_url_path="/static", static_folder=static_path)
    app.config.from_pyfile(config)
    from app.swagger import swaggerui_blueprint
    from app.urls import initial_blueprint

    register_extensions(app)
    v1_bp = Blueprint("v1", __name__, url_prefix="/v1")

    @v1_bp.route("/static/<path>")
    def send_static(path):
        return send_from_directory("static", path)

    initial_blueprint(v1_bp)
    app.register_blueprint(v1_bp)
    app.register_blueprint(swaggerui_blueprint)

    return app
