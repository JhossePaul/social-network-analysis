# from os import getenv
import settings as Config

from flask import Flask
from .models import SuperUser
from .extensions import db, login_manager, csrf
from .common import constants as COMMON_CONSTANTS
from .api import helloworld

# For import *
# __all__ = ['create_app']


DEFAULT_BLUEPRINTS = [
    helloworld,
]

def create_app(config = None, app_name = None, blueprints = None):
    """Create a Flask app."""
    if app_name is None:
        app_name = Config.DefaultConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_path = COMMON_CONSTANTS.INSTANCE_FOLDER_PATH, instance_relative_config = True)

    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_error_handlers(app)
    return app

def configure_app(app, config = None):
    """Different ways of configurations."""
    app.config.from_object(Config.DefaultConfig)
    if config:
        app.config.from_object(config)
    return

def configure_extensions(app):
    # Flask SQLAlchemy
    db.init_app(app)

    # Flask Login
    login_manager.login_view   = "frontend.index"
    login_manager.refresh.view = "frontend.index"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    login_manager.setup_app(app)

    # Flask WTF
    csrf.init_app(app)

def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def configure_logging(app):
    pass

def configure_hook(app):
    @app.before_request
    def before_request():
        pass

def configure_error_handlers(app):
    # example
    @app.errorhandler(500)
    def server_error_page(error):
        return "ERROR PAGE!"
