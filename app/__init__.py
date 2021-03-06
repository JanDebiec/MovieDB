import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
# from flask import jinja2.ext.loopcontrols
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log as admin in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    login.login_view = 'auth.login'

    migrate.init_app(app, db)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.mod_input.controllers import mod_input as input_module
    # Register blueprint(s)
    app.register_blueprint(input_module)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.mod_db.controllers import mod_db as db_module
    # Register blueprint(s)
    app.register_blueprint(db_module)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.mod_auth.controllers import mod_auth as auth_module
    # Register blueprint(s)
    app.register_blueprint(auth_module)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.mod_imdb.controllers import mod_imdb as imdb_module
    # Register blueprint(s)
    app.register_blueprint(imdb_module)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.mod_critics.controllers import mod_critics as critics_module
    # Register blueprint(s)
    app.register_blueprint(critics_module)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.main.controllers import mod_main as main_module
    # Register blueprint(s)
    app.register_blueprint(main_module)

    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    # if not app.debug and not app.testing:
    #     if app.config['LOG_TO_STDOUT']:
    #         stream_handler = logging.StreamHandler()
    #         stream_handler.setLevel(logging.INFO)
    #         app.logger.addHandler(stream_handler)
    #     else:
    #         if not os.path.exists('logs'):
    #             os.mkdir('logs')
    #         file_handler = RotatingFileHandler('logs/moviedb.log',
    #                                            maxBytes=10240, backupCount=10)
    #         file_handler.setFormatter(logging.Formatter(
    #             '%(asctime)s %(levelname)s: %(message)s '
    #             '[in %(pathname)s:%(lineno)d]'))
    #         file_handler.setLevel(logging.INFO)
    #         app.logger.addHandler(file_handler)
    #
    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('MovieDB startup')

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/moviedb.log',
                                       maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('MovieDB startup')

    return app


