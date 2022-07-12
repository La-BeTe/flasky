from flask import Flask
from flask_mail import Mail


from .models import db
from .configuration import Config
from .blueprints import Blueprint

mail = Mail()
config = Config()

def create_app(env):
    app = Flask(__name__)
    config.init_app(app, env)
    db.init_app(app)
    mail.init_app(app)
    Blueprint.init_app(app)
    return app
