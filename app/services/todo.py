# app/routes.py
from flask import Blueprint, request, abort, g
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from .. import db
from ..models import UserModel, TodoModel





todo_args = reqparse.RequestParser()
todo_args.add_argument('title', type=str, required=True, help="Title cannot be blank")
todo_args.add_argument('text', type=str, required=True, help="Text cannot be blank")
todo_args.add_argument('user_id', type=int, required=True, help="User ID cannot be blank")

todoFields = {
    'id': fields.Integer,
    'title': fields.String,
    'text': fields.String,
    'user_id': fields.Integer
}


class Todos(Resource):
    @marshal_with(todoFields)
    def get(self):
        # todos = TodoModel.query.filter_by(user_id=user_id).all()
        todos = TodoModel.query.all()
        if not todos:
            abort(404, description="No todos found")
        return todos

    @marshal_with(todoFields)
    def post(self):
        args = todo_args.parse_args()
        todo = TodoModel(title=args['title'], text=args['text'], user_id=args['user_id'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201

class Todo(Resource):
    @marshal_with(todoFields)
    def get(self, id):
        todo = TodoModel.query.filter_by(id=id).first()
        if not todo:
            abort(404, description="Todo not found")
        return todo

    @marshal_with(todoFields)
    def put(self, id):
        args = todo_args.parse_args()
        todo = TodoModel.query.filter_by(id=id).first()
        if not todo:
            abort(404, description="Todo not found")
        todo.title = args['title']
        todo.text = args['text']
        db.session.commit()
        return todo

    @marshal_with(todoFields)
    def delete(self, id):
        todo = TodoModel.query.filter_by(id=id).first()
        if not todo:
            abort(404, description="Todo not found")
        db.session.delete(todo)
        db.session.commit()
        return '', 204