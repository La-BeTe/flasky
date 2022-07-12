from flask import url_for

from . import db
from ._mixins import TimestampMixin

class Post(db.Model, TimestampMixin):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'body': self.body,
            'url': url_for('posts.get_post', id=self.id),
            'author': self.author.username,
            'comments': [comment.to_json() for comment in self.comments]
        }

    def __repr__(self):
        return f'<Post {self.id}>'