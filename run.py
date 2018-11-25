import os

from flask_migrate import Migrate

from src import create_app, db
from src.models import Role, User

app = create_app(os.getenv('FLASK_CONFIG', 'local'))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
