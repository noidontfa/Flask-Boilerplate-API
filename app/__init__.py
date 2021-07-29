from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()
migrate = Migrate()


def create_app(config="settings.py"):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile(config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


app = create_app()

from app import models