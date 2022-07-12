from flask import Blueprint, request, g

from app import config
from app.models import db
from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment
from app.utils import build_response, login_required
from app.schemas import validate, CREATE_POST_SCHEMA, CREATE_COMMENT_SCHEMA

posts = Blueprint('posts',  __name__)

@posts.route('/')
def get_posts():
    page = request.args.get('page', 1, int)
    author = request.args.get('author')
    query = Post.query
    if author:
        user = User.query.filter_by(username=author).first()
        query = Post.query.filter_by(author=user)
    posts = query.order_by(Post.created_at.desc()).paginate(page, config.FLASKY_POSTS_PER_PAGE, error_out=False)
    return build_response(200, 'Posts fetched successfully.', {
        'prev_page': posts.prev_num if posts.has_prev else None,
        'next_page': posts.next_num if posts.has_next else None,
        'posts': [post.to_json() for post in posts.items],
        'total_posts': posts.total
    })

@posts.route('/create', methods=['POST'])
@login_required
def create_post():
    params = validate(CREATE_POST_SCHEMA, request.get_json())
    post = Post(body=params['body'], author=g.user)
    db.session.add(post)
    db.session.commit()
    return build_response(201, 'Post created successfully.', post.to_json())


@posts.route('/<int:id>')
def get_post(id):
    post = Post.query.get(id)
    if not post:
        return build_response(404, 'Post not found.')
    return build_response(200, 'Post fetched successfully.', post.to_json())


@posts.route('/<int:id>/delete', methods=['DELETE'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id, author=g.user).first()
    if not post:
        return build_response(404, 'Post not found.')
    db.session.delete(post)
    db.session.commit()
    return build_response(200, 'Post deleted successfully.', post.to_json())

@posts.route('/<int:id>/update', methods=['PUT'])
@login_required
def update_post(id):
    params = validate(CREATE_POST_SCHEMA, request.get_json())
    post = Post.query.filter_by(id=id, author=g.user).first()
    if not post:
        return build_response(404, 'Post not found.')
    post.body = params['body']
    db.session.add(post)
    db.session.commit()
    return build_response(200, 'Post updated successfully.', post.to_json())

@posts.route('/<int:post_id>/comments', methods=['POST'])
@login_required
def add_comment(post_id):
    params = validate(CREATE_COMMENT_SCHEMA, request.get_json())
    comment = Comment(body=params['body'], author=g.user, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return build_response(201, 'Comment added successfully.', comment.to_json())

@posts.route('/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(post_id, comment_id):
    comment = Comment.query.filter_by(post_id=post_id, id=comment_id, author=g.user).first()
    if not comment:
        return build_response(404, 'Comment not found.')
    db.session.delete(comment)
    db.session.commit()
    return build_response(200, 'Comment deleted successfully.', comment.to_json())
