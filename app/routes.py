# app/routes.py
from flask import Blueprint, request, abort, g
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from .services.todo import Todos, Todo
from .services.user import Users, User
from .services.auth import Login, Register
from .services.cat import Cats, Cat

api_bp = Blueprint('api', __name__)
api = Api(api_bp)



api.add_resource(Users, '/users')
api.add_resource(User, '/user/<int:id>')

api.add_resource(Todos, '/todos')
api.add_resource(Todo, '/todo/<int:id>')

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')

api.add_resource(Cats, '/cats')
api.add_resource(Cat, '/cat/<int:id>')