from flask import Flask,request,abort

from flask_restful import Resource,Api,fields,marshal_with,reqparse

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)



class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    todos = db.relationship('TodoModel', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"User(name = {self.name}, email={self.email})"
    
class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)

    user = db.relationship('UserModel', back_populates='todos')

    def __repr__(self):
        return f"Todo(title = {self.title}, text={self.text})"
    
user_args = reqparse.RequestParser()
user_args.add_argument('name',type=str,required=True,help="Name cannot be blank")
user_args.add_argument('email',type=str,required=True,help="Email cannot be blank")

userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String
}

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


class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)    
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"],email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,message="User not found")
        return user
    
    @marshal_with(userFields)
    def put(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,message="User not found")
        user.name = args["name"]
        user.email= args["email"]
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,message="User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users
    
class Todos(Resource):
    @marshal_with(todoFields)
    def get(self, user_id):
        todos = TodoModel.query.filter_by(user_id=user_id).all()
        if not todos:
            abort(404, message="No todos found for this user")
        return todos

    @marshal_with(todoFields)
    def post(self, user_id):
        args = todo_args.parse_args()
        todo = TodoModel(title=args['title'], text=args['text'], user_id=user_id)
        db.session.add(todo)
        db.session.commit()
        return todo, 201

class Todo(Resource):
    @marshal_with(todoFields)
    def get(self, id):
        todo = TodoModel.query.filter_by(id=id).first()
        if not todo:
            abort(404, message="Todo not found")
        return todo

    @marshal_with(todoFields)
    def put(self, id):
        args = todo_args.parse_args()
        todo = TodoModel.query.filter_by(id=id).first()
        if not todo:
            abort(404, message="Todo not found")
        todo.title = args['title']
        todo.text = args['text']
        db.session.commit()
        return todo

    @marshal_with(todoFields)
    def delete(self, id):
        todo = TodoModel.query.filter_by(id=id).first()
        if not todo:
            abort(404, message="Todo not found")
        db.session.delete(todo)
        db.session.commit()
        return '', 204


api.add_resource(Users,'/api/users')
api.add_resource(User,'/api/user/<int:id>')

api.add_resource(Todos, '/api/user/<int:user_id>/todos')
api.add_resource(Todo, '/api/todo/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)

