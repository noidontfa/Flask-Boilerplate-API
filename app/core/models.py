import uuid

from sqlalchemy.dialects.postgresql import UUID

from app.extensions import bcrypt, db


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password=password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
