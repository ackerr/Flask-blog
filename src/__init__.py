from flask import Flask

from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    migrate.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from src.main import app as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
