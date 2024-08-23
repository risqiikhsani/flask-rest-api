from flask import Blueprint, jsonify, request, abort, g
from flask_jwt_extended import create_access_token
from flask_restful import Resource, Api, reqparse
from .. import db, bcrypt
from ..models import UserModel

# Argument parsing for login and registration
login_args = reqparse.RequestParser()
login_args.add_argument('username', type=str, required=True, help="Username cannot be blank")
login_args.add_argument('password', type=str, required=True, help="Password cannot be blank")

register_args = reqparse.RequestParser()
register_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
register_args.add_argument('username', type=str, required=True, help="Username cannot be blank")
register_args.add_argument('password', type=str, required=True, help="Password cannot be blank")
register_args.add_argument('email', type=str, required=True, help="Email cannot be blank")


class Register(Resource):
    def post(self):
        args = register_args.parse_args()
        # Check if the username or email already exists
        if UserModel.query.filter_by(username=args["username"]).first():
            return jsonify({'message': 'Username already exists'}), 400
        if UserModel.query.filter_by(email=args["email"]).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(args["password"]).decode('utf-8')
        
        # Create a new user
        user = UserModel(
            name=args["name"],
            username=args["username"],
            password=hashed_password,  # Store the hashed password
            email=args["email"]
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201


class Login(Resource):
    def post(self):
        args = login_args.parse_args()
        user = UserModel.query.filter_by(username=args["username"]).first()
        
        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, args["password"]):
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': 'Login Successful', 'access_token': access_token})
        else:
            return jsonify({'message': 'Login Failed'}), 401
