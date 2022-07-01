from flask import Blueprint, g, request

from app.models import db
from app.schemas import UPDATE_PASSWORD_SCHEMA
from app.utils import login_required, build_response, validate_payload, ValidationError, generate_token, send_email

account = Blueprint('account', __name__)

@account.route('/')
@login_required
def get_user():
    return build_response(200, 'User fetched successfully.', {
        'email': g.user.email,
        'username': g.user.username,
        'has_been_confirmed': bool(g.user.confirmed)
    })

@account.route('/confirm')
@login_required
def confirm_user():
    if g.user.confirmed:
        return build_response(400, 'User has already been confirmed.')
        
    token = generate_token({
        'user_id': g.user.id,
        'is_confirmation_token': True
    })
    send_email('Confirm Account', [g.user.email], 'confirm_account', user=g.user, token=token)
    return build_response(200, 'Confirmation email has been sent.')

@account.route('/password/update', methods=['POST'])
@login_required
def update_password():
    try:
        # We need to find a way to invalidate all tokens created previously after password updates
        # Temporary workaround is using 'updated' field in login token
        result = validate_payload(UPDATE_PASSWORD_SCHEMA, request.get_json())
        if result['old_password'] == result['new_password']:
            raise ValidationError('Old Password and New Password cannot be thesame.')
        if not g.user.verify_password(result['old_password']):
            raise ValidationError('Old Password is incorrect.')
        if result['new_password'] != result['confirm_password']:
            raise ValidationError('New Password and Confirm Password fields should be equal.')
    except ValidationError as err:
        return build_response(400, str(err))
    
    g.user.password = result['new_password']
    db.session.add(g.user)
    db.session.commit()
    return build_response(200, 'Password changed successfully.')