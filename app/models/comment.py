from flask import url_for

from . import db
from ._mixins import TimestampMixin

class Comment(db.Model, TimestampMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def to_json(self):
        return {
            'id': self.id,
            'body': self.body,
            'author': self.author.username,
            'delete_comment': url_for('posts.delete_comment', post_id=self.post_id, comment_id=self.id)
        }

    def __repr__(self):
        return f'<Comment {self.id}>'