# app/routes.py
from flask import Blueprint, request, abort, g
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from .services.todo import Todos, Todo
from .services.user import Users, User

api_bp = Blueprint('api', __name__)
api = Api(api_bp)



api.add_resource(Users, '/users')
api.add_resource(User, '/user/<int:id>')



api.add_resource(Todos, '/todos')
api.add_resource(Todo, '/todo/<int:id>')