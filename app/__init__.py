# app/__init__.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_strong_secret_key'
    app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    
    # https://github.com/vimalloc/flask-jwt-extended/issues/141#issuecomment-387319917
    app.config['PROPAGATE_EXCEPTIONS'] = True

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # @jwt.unauthorized_loader
    # def unauthorized_response(callback):
    #     return jsonify({
    #         'message': 'Missing or invalid JWT token. Please provide a valid token in the Authorization header.'
    #     }), 401

    with app.app_context():
        from .routes import api_bp
        app.register_blueprint(api_bp)

        db.create_all()

    return app
