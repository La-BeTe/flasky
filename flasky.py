import os
from dotenv import load_dotenv
from flask_migrate import Migrate

from app import create_app, db
from app.models import User, Role

load_dotenv()

app = create_app(os.getenv('FLASK_ENV'))

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Role': Role
    }