from app.core.urls import core_bp


def initial_blueprint(app):
    app.register_blueprint(core_bp)
