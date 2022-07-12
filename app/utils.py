import json
from functools import wraps
from flask import jsonify
from flask_mail import Message
from cerberus import Validator
from flask import render_template, request, g

from app import mail, config
from app.models import user, token

User = user.User
Token = token.Token

class ValidationError(Exception):
    pass

def build_response(status_code, message, data=None, headers={}):
    status_code = int(status_code)
    status = 'success' if status_code < 400 else 'error'
    message = str(message)
    if not message.endswith('.'):
        message += '.'
    return jsonify(status=status, message=message, data=data), status_code, headers

def validate_payload(schema, data):
    validator = Validator(schema, allow_unknown=True)
    result = validator.validated(data)
    if result is None:
        error_messages = []
        for key in validator.errors.keys():
            error_message_func = schema[key].get('meta') and (schema[key]['meta'].get('get_error_message'))
            error_message_str = schema[key].get('meta') and (schema[key]['meta'].get('error_message'))
            error_message = error_message_str
            if error_message_func:
                error_message = error_message_func(data)
            if error_message:
                error_messages.append(error_message)
        first_error_message = error_messages[0] if len(error_messages) > 0 else 'A validation error occurred.'
        raise ValidationError(first_error_message)
    return result

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
        data = Token.validate(auth_token)
        user = User.query.get(data.get('user_id')) if data and data.get('is_login_token') else None
        if not user or str(user.updated_at) != data.get('updated'):
            return build_response(401, 'Unauthorized request, please login.')
        g.user = user
        return f(*args, **kwargs)
    return wrapper
