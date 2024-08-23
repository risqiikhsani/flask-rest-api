# app/models.py
from . import db

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

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
