import json
from functools import wraps
from app.models import User
from cerberus import Validator
from flask_mail import Message
from flask import render_template, request, g
from itsdangerous import URLSafeTimedSerializer

from app import mail, config

class ValidationError(Exception):
    pass

def build_response(status_code, message, data=None):
    status_code = int(status_code)
    status = 'success' if status_code < 400 else 'error'
    message = str(message)
    if not message.endswith('.'):
        message += '.'
    return json.dumps({
        'status': status,
        'message': message,
        'data': data
    }), status_code, {
        'Content-Type': 'application/json'
    }

def validate_payload(schema, data):
    validator = Validator(schema, allow_unknown=True)
    result = validator.validated(data)
    if result is None:
        error_messages = [schema[x]['meta']['error_message'] for x in validator.errors.keys() if (schema[x].get('meta') and schema[x]['meta'].get('error_message'))]
        first_error_message = error_messages[0] if len(error_messages) > 0 else 'A validation error occurred.'
        raise ValidationError(first_error_message)
    return result

def send_email(subject, recipients, template, **kwargs):
    print(subject, recipients, template, kwargs)
    # Below has been tested and works but I'll work on the mailing templates with the frontend
    # So I'm printing arguments to the screen for now
    # msg = Message(f'{config.FLASKY_MAIL_SUBJECT_PREFIX} - {subject}', sender=config.FLASKY_MAIL_SENDER, recipients=recipients)
    # msg.body = render_template(f'mails/{template}.txt', **kwargs)
    # msg.html = render_template(f'mails/{template}.html', **kwargs)
    # mail.send(msg)

def generate_token(data, salt=None):
    salt = (config.FLASKY_SALT + str(salt)) if salt else config.FLASKY_SALT
    return URLSafeTimedSerializer(config.SECRET_KEY).dumps(data, salt)

def validate_token(token, expiration_in_minutes, salt=None):
    data = None
    salt = (config.FLASKY_SALT + str(salt)) if salt else config.FLASKY_SALT
    try:
        data = URLSafeTimedSerializer(config.SECRET_KEY).loads(token, max_age=expiration_in_minutes * 60, salt=salt)
    except Exception:
        return False
    return data

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get('auth_token')
        data = validate_token(token=auth_token, expiration_in_minutes=60)
        user = User.query.get(data.get('user_id')) if data and data.get('is_login_token') else None
        if not user or str(user.updated_at) != data.get('updated'):
            return build_response(401, 'User is not logged in.')
        g.user = user
        return f(*args, **kwargs)
    return wrapper
