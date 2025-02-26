from flask import Blueprint, request, abort, g
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from .. import db
from ..models import CatModel, TodoModel, CatModel



cat_args = reqparse.RequestParser()
cat_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
cat_args.add_argument('age', type=int, required=True, help="Age cannot be blank")
cat_args.add_argument('color', type=str, required=True, help="Color cannot be blank")

catFields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'color': fields.String
}

class Cats(Resource):
    @marshal_with(catFields)
    def get(self):
        cats = CatModel.query.all()
        return cats

    @marshal_with(catFields)
    def post(self):
        args = cat_args.parse_args()
        cat = CatModel(name=args["name"], age=args["age"], color=args["color"])
        db.session.add(cat)
        db.session.commit()
        cats = CatModel.query.all()
        return cats, 201

class Cat(Resource):
    @marshal_with(catFields)
    def get(self, id):
        cat = CatModel.query.filter_by(id=id).first()
        if not cat:
            abort(404, description="cat not found")
        return cat

    @marshal_with(catFields)
    def put(self, id):
        args = cat_args.parse_args()
        cat = CatModel.query.filter_by(id=id).first()
        if not cat:
            abort(404, description="cat not found")
        cat.name = args["name"]
        cat.age = args["age"]
        cat.color = args["color"]
        db.session.commit()
        return cat

    @marshal_with(catFields)
    def delete(self, id):
        cat = CatModel.query.filter_by(id=id).first()
        if not cat:
            abort(404, description="cat not found")
        db.session.delete(cat)
        db.session.commit()
        cats = CatModel.query.all()
        return cats