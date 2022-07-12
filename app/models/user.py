from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from ._mixins import TimestampMixin

class User(db.Model, TimestampMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=0)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @property
    def password(self):
        pass

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            'email': self.email,
            'username': self.username,
            'has_been_confirmed': bool(self.confirmed),
            'member_since': self.created_at,
            'posts': [post.to_json() for post in self.posts]
        }


    def __repr__(self):
        return f'<User {self.username}>'
