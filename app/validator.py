from copy import deepcopy
from cerberus import Validator

class ValidationError(ValueError):
    pass

def custom_confirm_password_validator(data):
    password = data.get('password') or data.get('new_password')
    confirm_password = data.get('confirm_password')
    if password != confirm_password:
        raise ValidationError('Password and Confirm Password fields should be equal.')


def custom_update_password_validator(data):
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    if old_password == new_password:
        raise ValidationError('Old Password and New Password cannot be thesame.')

def validate(schema, data):
    schema = deepcopy(schema)
    custom_validators = schema.pop('custom_validators', [])
    validator = Validator(schema, allow_unknown=True)
    result = validator.validated(data)
    if result is None:
        error_messages = []
        for key in validator.errors.keys():
            error_message = schema[key].get('meta') and (schema[key]['meta'].get('error_message'))
            if callable(error_message):
                error_message = error_message(data, validator.errors[key])
            if isinstance(error_message, str):
                error_messages.append(error_message)
        first_error_message = error_messages[0] if len(error_messages) > 0 else 'A validation error occurred.'
        raise ValidationError(first_error_message)
    
    for custom_validator in custom_validators:
        custom_validator(data)

    return result

SCHEMAS = {
    'DEFAULT': {
        'email': {
            'type': 'string',
            'required': True,
            'regex': r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
            'meta': {
                'error_message': 'Email is invalid.'
            }
        },
        'username': {
            'type': 'string',
            'required': True,
            'regex': r'^[a-zA-Z][\w]{5,}$',
            'meta': {
                'error_message': 'Username must contain more than 5 characters, start with a letter and can only contain letters, numbers or underscores.'
            }
        },
        'password': {
            'type': 'string',
            'required': True,
            'regex': r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
            'meta': {
                'error_message': 'Password must contain one uppercase letter, one lowercase letter, one number and a special symbol.'
            }
        },
        'confirm_password': {
            'type': 'string',
            'required': True,
            'meta': {
                'error_message': 'Password confirmation is required.'
            }
        },
        'custom_validators': [custom_confirm_password_validator]
    }
}

SCHEMAS['REGISTER'] = SCHEMAS['DEFAULT']

SCHEMAS['LOGIN'] = {
    'email': {
        'type': 'string',
        'required': True,
        'meta': {
            'error_message': 'Email is required.'
        }
    },
    'password': {
        'type': 'string',
        'required': True,
        'meta': {
            'error_message': 'Password is required.'
        }
    }
}

SCHEMAS['UPDATE_PASSWORD'] = {
    'old_password': {
        'type': 'string',
        'required': True,
        'empty': False,
        'meta': {
            'error_message': 'Old password is required.'
        }
    },
    'new_password': SCHEMAS['DEFAULT']['password'],
    'confirm_password': SCHEMAS['DEFAULT']['confirm_password'],
    'custom_validators': [
        custom_update_password_validator,
        custom_confirm_password_validator
    ] 
}

SCHEMAS['RESET_PASSWORD_START'] = {
    'email': SCHEMAS['DEFAULT']['email']
}

SCHEMAS['RESET_PASSWORD_END'] = {
    'new_password': SCHEMAS['DEFAULT']['password'],
    'confirm_password': SCHEMAS['DEFAULT']['confirm_password']
}

SCHEMAS['POST'] = {
    'body': {
        'type': 'string',
        'required': True,
        'empty': False,
        'meta': {
            'error_message': 'Post body is required.'
        }
    }
}
SCHEMAS['COMMENT'] = {
    'body': {
        'type': 'string',
        'required': True,
        'empty': False,
        'meta': {
            'error_message': 'Comment body is required.'
        }
    }
}