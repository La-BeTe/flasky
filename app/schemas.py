from cerberus import Validator

class ValidationError(ValueError):
    pass


def validate_confirm_password(data):
    password = data.get('password') or data.get('new_password')
    confirm_password = data.get('confirm_password')
    if password != confirm_password:
            raise ValidationError('Password and Confirm Password fields should be equal.')

def validate(schema, data):
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
    for field in schema:
        value = schema[field]
        func = value.get('meta') and value['meta'].get('custom_validator')
        if func:
            func(data)
    return result

REGISTER_SCHEMA = {
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
            'error_message': 'Password confirmation is required.',
            'custom_validator': validate_confirm_password
        }
    }
}


LOGIN_SCHEMA = {
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

UPDATE_PASSWORD_SCHEMA = {
    'old_password': {
        'type': 'string',
        'required': True,
        'meta': {
            'error_message': 'Old password is required.'
        }
    },
    'new_password': REGISTER_SCHEMA['password'],
    'confirm_password': REGISTER_SCHEMA['confirm_password']
}

RESET_PASSWORD_START_SCHEMA = {
    'email': REGISTER_SCHEMA['email']
}

RESET_PASSWORD_END_SCHEMA = {
    'new_password': REGISTER_SCHEMA['password'],
    'confirm_password': REGISTER_SCHEMA['confirm_password']
}

CREATE_POST_SCHEMA = {
    'body': {
        'type': 'string',
        'required': True,
        'empty': False,
        'meta': {
            'error_message': 'Post body is required.'
        }
    }
}
CREATE_COMMENT_SCHEMA = {
    'body': {
        'type': 'string',
        'required': True,
        'empty': False,
        'meta': {
            'error_message': 'Comment body is required.'
        }
    }
}

