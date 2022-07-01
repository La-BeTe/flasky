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
        'regex': r'^[a-zA-Z][\w]{6,}$',
        'meta': {
            'error_message': 'Username must start with a letter and can only contain letters, numbers or underscores.'
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