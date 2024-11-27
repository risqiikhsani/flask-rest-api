from flask import Blueprint, request, abort
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import TodoModel

# Parser for todo fields
todo_args = reqparse.RequestParser()
todo_args.add_argument('title', type=str)
todo_args.add_argument('text', type=str)

# Fields to be serialized
todoFields = {
    'id': fields.Integer,
    'title': fields.String,
    'text': fields.String,
    'user_id': fields.Integer
}


class Todos(Resource):
    @marshal_with(todoFields)
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        todos = TodoModel.query.filter_by(user_id=user_id).all()
        return todos

    @marshal_with(todoFields)
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        args = todo_args.parse_args()
        todo = TodoModel(title=args['title'], text=args['text'], user_id=user_id)
        db.session.add(todo)
        db.session.commit()
        return todo, 201

class Todo(Resource):
    @marshal_with(todoFields)
    @jwt_required()
    def get(self, id):
        user_id = get_jwt_identity()
        todo = TodoModel.query.filter_by(id=id, user_id=user_id).first()
        if not todo:
            abort(404, description="Todo not found")
        return todo

    @marshal_with(todoFields)
    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()
        args = todo_args.parse_args()
        todo = TodoModel.query.filter_by(id=id, user_id=user_id).first()
        if not todo:
            abort(404, description="Todo not found")
        if args["title"]:
            todo.title = args['title']
        if args["text"]:
            todo.text = args['text']
        db.session.commit()
        return todo

    @marshal_with(todoFields)
    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        todo = TodoModel.query.filter_by(id=id, user_id=user_id).first()
        if not todo:
            abort(404, description="Todo not found")
        db.session.delete(todo)
        db.session.commit()
        return '', 204

