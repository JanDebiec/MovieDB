from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # db.init_app(app)
    bootstrap.init_app(app)

    migrate.init_app(app, db)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.userinput.controllers import mod_input as input_module
    # Register blueprint(s)
    app.register_blueprint(input_module)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.db import bp as db_bp
    # Register blueprint(s)
    app.register_blueprint(db_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    return app


from app import models
from app.main import routes
from app.userinput import handler as ush
from app.db import handler as dbh

