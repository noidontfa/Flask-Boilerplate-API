from flask_mail import email_dispatched

from app.app import create_app

app = create_app()


def log_message(message, app):
    app.logger.debug(message)


email_dispatched.connect(log_message)
