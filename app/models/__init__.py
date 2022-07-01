from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=datetime.utcnow, default=datetime.utcnow)

class Role(db.Model, TimestampMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model, TimestampMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=0)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    @property
    def role(self):
        user_role = Role.query.get(self.role_id)
        if not user_role:
            raise RuntimeError('Invalid user role.')
        return user_role.name

    @role.setter
    def role(self, role_name):
        user_role = Role.query.filter_by(name=role_name).first()
        if not user_role:
            raise RuntimeError('Invalid user role.')
        self.role_id = user_role.id

    @property
    def password(self):
        pass

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

