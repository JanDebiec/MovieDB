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
    from app.db.controllers import mod_db as db_module
    # Register blueprint(s)
    app.register_blueprint(db_module)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.main.controllers import mod_main as main_module
    # Register blueprint(s)
    app.register_blueprint(main_module)

    return app


