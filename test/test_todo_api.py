import pytest
from app import create_app, db
from app.models import CatModel, TodoModel, UserModel
from flask_jwt_extended import create_access_token
import tempfile
import os



        
@pytest.fixture
def init_database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Create a dummy user and todos
        user = UserModel(username='testuser', password='testpassword', name='testuser', email="testuser@gmail.com")
        db.session.add(user)
        db.session.commit()
        
        # Create some todos associated with the user
        todo1 = TodoModel(title='first', text='first todo', user_id=user.id)
        todo2 = TodoModel(title='second', text='second todo', user_id=user.id)
        db.session.add(todo1)
        db.session.add(todo2)
        db.session.commit()
        
        yield db, user  # this is where the testing happens!
        
    with app.app_context():
        db.session.remove()
        db.drop_all()
        
@pytest.fixture
def jwt_token(app, init_database):
    db, user = init_database
    with app.app_context():
        access_token = create_access_token(identity=user.id)
        return access_token
        

def test_get_all_todos(client, jwt_token):
    response = client.get('/todos', headers={'Authorization': f'Bearer {jwt_token}'})
    assert response.status_code == 200
    assert len(response.json) == 2

def test_post_todo(client,  jwt_token):
    todo_data = {'title': 'Write tests', 'text': 'Write unit tests for the API'}
    response = client.post('/todos', json=todo_data, headers={'Authorization': f'Bearer {jwt_token}'})
    assert response.status_code == 201
    assert response.json['title'] == 'Write tests'
    assert response.json['text'] == 'Write unit tests for the API'

# def test_get_single_todo(client, init_database, jwt_token):
#     response = client.get('/todo/1', headers={'Authorization': f'Bearer {jwt_token}'})
#     assert response.status_code == 200
#     assert response.json['title'] == 'first'

# def test_get_single_todo_not_found(client, jwt_token):
#     response = client.get('/todo/999', headers={'Authorization': f'Bearer {jwt_token}'})
#     assert response.status_code == 404
#     assert response.json['message'] == 'Todo not found'

# def test_put_todo(client, init_database, jwt_token):
#     updated_data = {'title': 'Buy groceries', 'text': 'Get groceries for the week'}
#     response = client.put('/todo/1', json=updated_data, headers={'Authorization': f'Bearer {jwt_token}'})
#     assert response.status_code == 200
#     assert response.json['title'] == 'Buy groceries'
#     assert response.json['text'] == 'Get groceries for the week'

# def test_put_todo_not_found(client, jwt_token):
#     updated_data = {'title': 'Buy groceries', 'text': 'Get groceries for the week'}
#     response = client.put('/todo/999', json=updated_data, headers={'Authorization': f'Bearer {jwt_token}'})
#     assert response.status_code == 404
#     assert response.json['message'] == 'Todo not found'

# def test_delete_todo(client, init_database, jwt_token):
#     response = client.delete('/todo/1', headers={'Authorization': f'Bearer {jwt_token}'})
#     assert response.status_code == 204

# def test_delete_todo_not_found(client, jwt_token):
#     response = client.delete('/todo/999', headers={'Authorization': f'Bearer {jwt_token}'})
#     assert response.status_code == 404
#     assert response.json['message'] == 'Todo not found'
