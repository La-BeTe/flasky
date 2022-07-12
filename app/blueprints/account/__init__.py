from flask import Blueprint, g, request

from app.models import db, token
from app.validator import SCHEMAS, validate, ValidationError
from app.utils import login_required, build_response, send_email

Token = token.Token
account = Blueprint('account', __name__)

@account.route('/')
@login_required
def get_user():
    return build_response(200, 'User fetched successfully.', g.user.to_json())

@account.route('/confirm')
@login_required
def confirm_user():
    if g.user.confirmed:
        return build_response(400, 'User has already been confirmed.')    
    token = Token.create(data={
        'user_id': g.user.id,
        'is_confirmation_token': True
    }, expiration_in_minutes=360)
    send_email('Confirm Account', [g.user.email], 'confirm_account', user=g.user, token=token)
    return build_response(200, 'Confirmation email has been sent.')

@account.route('/password/update', methods=['POST'])
@login_required
def update_password():
    # We need to find a way to invalidate all tokens created previously after password updates
    # Temporary workaround is using 'updated' field in login token
    result = validate(SCHEMAS['UPDATE_PASSWORD'], request.get_json())
    if not g.user.verify_password(result['old_password']):
        raise ValidationError('Old Password is incorrect.')
    g.user.password = result['new_password']
    db.session.add(g.user)
    db.session.commit()
    return build_response(200, 'Password changed successfully.')
