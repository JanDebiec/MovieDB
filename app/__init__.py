from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # db.init_app(app)
    migrate.init_app(app, db)

    from app.userinput import bp as user_bp
    app.register_blueprint(user_bp)

    from app.db import bp as db_bp
    app.register_blueprint(db_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    return app


from app import models
from app.main import routes
from app.userinput import handler as ush
from app.db import handler as dbh

