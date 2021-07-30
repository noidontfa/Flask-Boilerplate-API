from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def create_app(config="settings.py"):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile(config)

    from app.urls import initial_blueprint

    initial_blueprint(app)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
