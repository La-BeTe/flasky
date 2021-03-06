from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from app.models import db, user, token, role
from app.utils import build_response, send_email
from app.validator import validate, SCHEMAS

User = user.User
Token = token.Token
Role = role.Role
auth = Blueprint('auth',  __name__)

@auth.route('/register', methods=['POST'])
def register():
    try:
        params = validate(SCHEMAS['REGISTER'], request.get_json())
        new_user = User(email=params['email'], username=params['username'])
        new_user.role = Role.query.filter_by(name='User').first()
        new_user.password = params['password']
        db.session.add(new_user)
        db.session.commit()
        token = Token.create(data={
            'user_id': new_user.id,
            'is_confirmation_token': True
        }, expiration_in_minutes=360)
        send_email('Confirm Account', [new_user.email], 'confirm_account', user=new_user, token=token)
        return build_response(200, 'User registration successful, please check your email to confirm email address.')
    except IntegrityError as err:
        if str(err).find('Duplicate entry') >= 0:
            return build_response(400, "User with email or username already exists.")
        raise err


@auth.route('/login', methods=['POST'])
def login():
    params = validate(SCHEMAS['LOGIN'], request.get_json())
    user = User.query.filter_by(email=params['email']).first()
    is_password_valid = user and user.verify_password(params['password'])
    if not is_password_valid:
        return build_response(400, 'Email and password do not match.')

    token = Token.create(data={
        'user_id': user.id,
        'is_login_token': True,
        'updated': str(user.updated_at)
    }, expiration_in_minutes=60)
    return build_response(200, 'User login successful.', {
        'auth_token': token
    })

@auth.route('/confirm/<token>')
def confirm(token):
    is_valid_token = Token.validate(token, 'is_confirmation_token')
    if is_valid_token and is_valid_token.get('user_id'):
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
    params = validate(SCHEMAS['RESET_PASSWORD_START'], request.get_json())
    user = User.query.filter_by(email=params['email']).first()
    if not user:
        return build_response(400, f"User with email {params['email']} does not exist.")

    token = Token.create(data={
        'email': params['email'],
        'is_reset_token': True
    }, expiration_in_minutes=360)
    send_email('Reset Password', [params['email']], 'reset_password', token=token)
    return build_response(200, 'Password reset email has been sent to user.')

@auth.route('/password/reset/<token>', methods=['POST'])
def reset_password_end(token):
    params = validate(SCHEMAS['RESET_PASSWORD_END'], request.get_json())
    data = Token.validate(token, 'is_reset_token')
    user = User.query.filter_by(email=data.get('email')).first() if data else None
    if not user:
        return build_response(400, 'Token is invalid or has expired.')
    user.password = params['new_password']
    db.session.add(user)
    db.session.commit()
    return build_response(200, 'Password reset successful.')
