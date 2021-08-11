import uuid
from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import UUID

from app import settings
from app.core.model_utils import TimestampedModel
from app.core.utils import random_with_n_digits
from app.extensions import bcrypt, db


class User(TimestampedModel):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    is_email_verified = db.Column(db.Boolean(), default=False)
    email_address = db.relationship(
        "EmailAddress", backref="user", cascade="all,delete", uselist=False
    )
    reset_password = db.relationship(
        "ResetPassword", backref="user", cascade="all,delete", uselist=False
    )

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password=password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class EmailAddress(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255))
    key = db.Column(db.String(64))
    sent = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def key_expired(self):
        expiration_date = self.sent + timedelta(
            days=settings.EMAIL_CONFIRMATION_EXPIRE_DAYS
        )
        return expiration_date <= datetime.now()

    def confirm(self, key):
        if not self.key_expired() and self.key == key:
            user = User.query.filter_by(email=self.email).first()
            if user.is_email_verified:
                return None
            user.is_email_verified = True
            user.save()
            return user
        return None

    def generate_key(self):
        self.key = random_with_n_digits(6)
        self.sent = datetime.now()
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ResetPassword(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = db.Column(db.String(64))
    sent = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def set_new_password(self, key, password):
        if self.key == key:
            user = User.query.get(self.user_id)
            user.set_password(password)
            user.save()
            return True
        return None

    def generate_key(self):
        self.key = random_with_n_digits(6)
        self.sent = datetime.now()
        db.session.commit()
        return self

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
