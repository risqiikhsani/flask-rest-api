import pytest
from app import create_app, db
from app.models import CatModel


# @pytest.fixture(scope='module')
# def test_client():
#     flask_app = create_app('testing')
#     testing_client = flask_app.test_client()
    
#     # Establish an application context before running the tests.
#     with flask_app.app_context():
#         db.create_all()  # Create tables

#     yield testing_client  # this is where the testing happens!

#     # Tear down the database after the tests
#     with flask_app.app_context():
#         db.drop_all()
        
        
        
@pytest.fixture
def init_database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        cat1 = CatModel(name='Whiskers', age=3, color='black')
        cat2 = CatModel(name='Mittens', age=5, color='orange')
        db.session.add(cat1)
        db.session.add(cat2)
        db.session.commit()
    
    yield db  # this is where the testing happens!
    
    with app.app_context():
        db.session.remove()
        db.drop_all()
    

def test_get_all_cats(client,init_database):
    response = client.get('/cats')
    assert response.status_code == 200
    assert len(response.json) == 2
    
def test_post_cat(client):
    cat_data = {'name': 'Fluffy', 'age': 2, 'color': 'orange'}
    response = client.post('/cats', json=cat_data)
    assert response.status_code == 201
    assert response.json[0]['name'] == 'Fluffy'
    assert response.json[0]['age'] == 2
    assert response.json[0]['color'] == 'orange'
    

def test_get_single_cat(client, init_database):
    response = client.get('/cat/1')
    assert response.status_code == 200
    assert response.json['name'] == 'Whiskers'
    assert response.json['age'] == 3
    assert response.json['color'] == 'black'

def test_get_single_cat_not_found(client):
    response = client.get('/cat/999')
    assert response.status_code == 404
    assert response.json['message'] == 'cat not found'

def test_put_cat(client, init_database):
    updated_data = {'name': 'Tommy', 'age': 4, 'color': 'gray'}
    response = client.put('/cat/1', json=updated_data)
    assert response.status_code == 200
    assert response.json['name'] == 'Tommy'
    assert response.json['age'] == 4
    assert response.json['color'] == 'gray'

def test_put_cat_not_found(client):
    updated_data = {'name': 'Tommy', 'age': 4, 'color': 'gray'}
    response = client.put('/cat/999', json=updated_data)
    assert response.status_code == 404
    assert response.json['message'] == 'cat not found'

def test_delete_cat(client, init_database):
    response = client.delete('/cat/1')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'Mittens'

def test_delete_cat_not_found(client):
    response = client.delete('/cat/999')
    assert response.status_code == 404
    assert response.json['message'] == 'cat not found'

