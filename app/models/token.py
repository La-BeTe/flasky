from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

from . import db
from app import config
from ._mixins import TimestampMixin

class Token(db.Model, TimestampMixin):
    __tablename__ = 'tokens'
    id = db.Column(db.String(256), primary_key=True)
    token = db.Column(db.Text, nullable=False)
    salt = db.Column(db.Text, nullable=True)
    expiration = db.Column(db.Integer, nullable=False)

    @staticmethod
    def update(tok, data):
        token_row = Token.query.get(tok)
        if not token_row:
            return
        token = URLSafeTimedSerializer(config.SECRET_KEY).dumps(data, token_row.salt)
        token_row.token = token
        db.session.add(token_row)
        db.session.commit()


    @staticmethod
    def create(data, expiration_in_minutes, salt=None):
        token = Token()
        salt = (config.FLASKY_SALT + str(salt)) if salt else config.FLASKY_SALT
        token.salt = salt
        _token = URLSafeTimedSerializer(config.SECRET_KEY).dumps(data, salt)
        token.token = _token
        token.expiration = expiration_in_minutes * 60
        HASH_METHOD = 'pbkdf2:sha256:30000'
        token.id = generate_password_hash(_token, HASH_METHOD).replace(f'{HASH_METHOD}$', '').upper()
        token.id = f'{config.TOKEN_PREPEND_STR}{token.id}'
        db.session.add(token)
        db.session.commit()
        return token.id

    @staticmethod
    def validate(tok):
        token_row = Token.query.get(tok)
        if not token_row:
            return False
        data = None
        token = token_row.token
        salt = token_row.salt
        max_age = token_row.expiration
        try:
            data = URLSafeTimedSerializer(config.SECRET_KEY).loads(token, max_age, salt=salt)
        except Exception:
            return False
        return data