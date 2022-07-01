from datetime import datetime
from flask import Blueprint, request

from app.models import User, db
from app.schemas import REGISTER_SCHEMA, LOGIN_SCHEMA, RESET_PASSWORD_START_SCHEMA, RESET_PASSWORD_END_SCHEMA
from app.utils import build_response, validate_payload, ValidationError, send_email, generate_token, validate_token

auth = Blueprint('auth',  __name__)

@auth.route('/register', methods=['POST'])
def register():
    try:
        params = validate_payload(REGISTER_SCHEMA, request.get_json())
        if params['password'] != params['confirm_password']:
            raise ValidationError('Password and Confirm Password fields should be equal.')

        new_user = User(email=params['email'], username=params['username'])
        new_user.role = 'User'
        new_user.password = params['password']
        db.session.add(new_user)
        db.session.commit()
        token = generate_token({
            'user_id': new_user.id,
            'is_confirmation_token': True
        })
        send_email('Confirm Account', [new_user.email], 'confirm_account', user=new_user, token=token)
        return build_response(200, 'User registration successful, please check your email to confirm email address.')
    except ValidationError as err:
        return build_response(400, str(err))
    except Exception as err:
        if str(err).find('Duplicate entry') >= 0:
            return build_response(400, f"User with email or username already exists.")
        raise err


@auth.route('/login', methods=['POST'])
def login():
    try:
        params = validate_payload(LOGIN_SCHEMA, request.get_json())
    except ValidationError as err:
        return build_response(400, str(err))
    
    user = User.query.filter_by(email=params['email']).first()
    is_password_valid = user and user.verify_password(params['password'])
    if not is_password_valid:
        return build_response(400, 'Email and password do not match.')

    token = generate_token({
        'user_id': user.id,
        'is_login_token': True,
        'updated': str(user.updated_at)
    })
    return build_response(200, 'User login successful.', {
        'auth_token': token
    })

@auth.route('/confirm/<token>')
def confirm(token):
    is_valid_token = validate_token(token, 360)
    if is_valid_token and is_valid_token.get('is_confirmation_token') and is_valid_token.get('user_id'):
        user_id = is_valid_token['user_id']
        user = User.query.get(user_id)
        if user.confirmed:
            return build_response(400, 'User has already been confirmed.')
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        return build_response(200, 'User email confirmation successful.')
    else:
        return build_response(400, 'Invalid token or token has expired.')

@auth.route('/password/reset/start', methods=['POST'])
def reset_password_start():
    try:
        params = validate_payload(RESET_PASSWORD_START_SCHEMA, request.get_json())
    except ValidationError as err:
        return build_response(400, str(err))
    
    user = User.query.filter_by(email=params['email']).first()
    if not user:
        return build_response(400, f"User with email {params['email']} does not exist.")

    token = generate_token({
        'email': params['email'],
        'is_reset_token': True
    })
    send_email('Reset Password', [params['email']], 'reset_password', token=token)
    return build_response(200, 'Password reset email has been sent to user.')

@auth.route('/password/reset/<token>', methods=['POST'])
def reset_password_end(token):
    try:
        params = validate_payload(RESET_PASSWORD_END_SCHEMA, request.get_json())
        if params['new_password'] != params['confirm_password']:
            raise ValidationError('Password and Confirm Password fields should be equal.')
    except ValidationError as err:
        return build_response(400, str(err))
    
    data = validate_token(token, expiration_in_minutes=360)
    user = User.query.filter_by(email=data.get('email')).first() if data and data.get('is_reset_token') else None
    if not user:
        return build_response(400, 'Token is invalid or has expired.')
    user.password = params['new_password']
    db.session.add(user)
    db.session.commit()
    return build_response(200, 'Password reset successful.')