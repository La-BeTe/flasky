import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')
    FLASKY_SALT = os.getenv('FLASKY_SALT') or 'e552e9206e61dbae552e9206e61dba5b5005b4180fa7242e552e9206e61dba5b5005b4180fa7242e552e9206e61dba5b5005b4180fa72425b5005b4180fa7242'
    FLASKY_MAIL_SUBJECT_PREFIX = os.getenv('FLASKY_MAIL_SUBJECT_PREFIX') or 'Flasky'
    FLASKY_MAIL_SENDER = os.getenv('MAIL_SENDER') or 'admin@flasky.com'
    TOKEN_PREPEND_STR = os.getenv('TOKEN_PREPEND_STR') or 'TOK-'
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True if os.getenv('MAIL_USE_TLS') == '1' else False
    MAIL_USE_SSL = True if os.getenv('MAIL_USE_SSL') == '1' else False
    FLASKY_POSTS_PER_PAGE = int(os.getenv('FLASKY_POSTS_PER_PAGE') or 20)


    def init_app(self, app, env):
        if env == 'development':
            self.DEBUG = True
        elif env == 'test':
            self.TESTING = True
        app.config.from_object(self)
