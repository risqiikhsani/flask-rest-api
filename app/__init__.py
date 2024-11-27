# app/__init__.py
from datetime import timedelta
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
migrate = Migrate() 


def create_app(env="development"):
    app = Flask(__name__)
    
    if env == "development":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
    elif env == "testing":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    elif env == "production":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/production_db'



    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_strong_secret_key'
    app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    
    # https://github.com/vimalloc/flask-jwt-extended/issues/141#issuecomment-387319917
    app.config['PROPAGATE_EXCEPTIONS'] = True

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    # Configure CORS to allow all origins
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # @jwt.unauthorized_loader
    # def unauthorized_response(callback):
    #     return jsonify({
    #         'message': 'Missing or invalid JWT token. Please provide a valid token in the Authorization header.'
    #     }), 401

    with app.app_context():
        from .routes import api_bp
        app.register_blueprint(api_bp)

        # db.create_all()

    return app
