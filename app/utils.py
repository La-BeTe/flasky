from functools import wraps
from flask import jsonify
from flask_mail import Message
from flask import render_template, request, g

from app import mail, config
from app.models import user, token

User = user.User
Token = token.Token

def build_response(status_code, message, data=None, headers={}):
    status_code = int(status_code)
    status = 'success' if status_code < 400 else 'error'
    message = str(message)
    if not message.endswith('.'):
        message += '.'
    return jsonify(status=status, message=message, data=data), status_code, headers

def send_email(subject, recipients, template, **kwargs):
    return print(subject, recipients, template, kwargs)
    # Below has been tested and works but I'll work on the mailing templates with the frontend
    # So I'm printing arguments to the screen for now
    msg = Message(f'{config.FLASKY_MAIL_SUBJECT_PREFIX} - {subject}', sender=config.FLASKY_MAIL_SENDER, recipients=recipients)
    msg.body = render_template(f'mails/{template}.txt', **kwargs)
    msg.html = render_template(f'mails/{template}.html', **kwargs)
    mail.send(msg)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get('auth_token')
        data = Token.validate(auth_token, 'is_login_token')
        user = User.query.get(data.get('user_id')) if data else None
        if not user or str(user.updated_at) != data.get('updated'):
            return build_response(401, 'Unauthorized request, please login.')
        g.user = user
        return f(*args, **kwargs)
    return wrapper
