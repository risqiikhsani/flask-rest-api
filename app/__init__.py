import os

from flask import Flask

from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_cors import CORS
from app.common import log_handlers
from flask_talisman import Talisman
from app import config
from app.models import db


# Initialize extensions



def create_app():
    app = Flask(__name__)
    
    app.config.from_object(config)
    # Initialize extensions
    db.init_app(app)
    
    jwt = JWTManager()
    bcrypt = Bcrypt()
    migrate = Migrate()
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    
    Talisman(app)
    CORS(app)

    # Register blueprints
    with app.app_context():
        from .routes import api_bp
        app.register_blueprint(api_bp)
        
    # Set up logging for production
    log_handlers.init_logging(app, "gunicorn.error")
    app.logger.info(70 * "*")
    app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
    app.logger.info(70 * "*")


    return app
