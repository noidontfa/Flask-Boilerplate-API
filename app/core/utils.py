from random import randint

from flask import render_template
from flask_mail import Message

from app import app, settings
from app.extensions import mail


def send_mail(subject, template_name, context, email, attach=None):

    body = render_template(
        template_name,
        **context,
    )
    to = [email] if isinstance(email, str) else email
    msg = Message(
        subject=subject, html=body, sender=settings.MAIL_DEFAULT_SENDER, recipients=to
    )
    if attach:
        with app.open_resource(attach) as fp:
            msg.attach(attach, data=fp.read())
    mail.send(msg)


def random_with_n_digits(n, is_testing=None):
    if is_testing:
        return 666666
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)
