import pytest
import werkzeug
from importlib.metadata import version
from app import app, db
from models.model_tables import Character


if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = version("werkzeug")

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()

    with app.test_client() as testing_client:
        yield testing_client
        with app.app_context():
            db.session.remove()
            db.drop_all()



@pytest.fixture(scope='function')
def init_database():
    db.session.add(Character(name="Jon Snow", house="Stark", role="Lord Commander", age=30))
    db.session.add(Character(name="Daenerys Targaryen", house="Targaryen", role="Queen", age=25))
    db.session.commit()

    yield

    db.session.remove()
    db.drop_all()


def test_home_route(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Game of Thrones Flask API!" in response.data


def test_list_characters(test_client, init_database):
    response = test_client.get('/characters/list')
    assert response.status_code == 200
    data = response.get_json()
    assert "total" in data
    assert data["total"] == 2

"""
def test_fetch_character_by_id(test_client, init_database):
    response = test_client.get('/characters/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Jon Snow"
    assert data["house"] == "Stark"

    response = test_client.get('/characters/99')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Character not found"

def test_fetch_filtered_characters(test_client, init_database):
    response = test_client.get('/characters/filter?name=Jon')
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["data"][0]["name"] == "Jon Snow"

    response = test_client.get('/characters/filter?house=Targaryen')
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["data"][0]["name"] == "Daenerys Targaryen"

def test_add_character(test_client):
    new_character = {
        "name": "Arya Stark",
        "house": "Stark",
        "role": "Assassin",
        "age": 18
    }
    response = test_client.post('/characters/add', json=new_character)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Arya Stark"
    assert data["house"] == "Stark"

def test_edit_character(test_client, init_database):
    updated_data = {
        "name": "Jon Targaryen",
        "age": 31
    }
    response = test_client.put('/characters/edit/1', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Jon Targaryen"
    assert data["age"] == 31

    response = test_client.put('/characters/edit/99', json=updated_data)
    assert response.status_code == 404
    assert response.get_json()["error"] == "Character with ID 99 not found"

def test_remove_character(test_client, init_database):
    response = test_client.delete('/characters/delete/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Character with ID 1 deleted successfully"

    response = test_client.delete('/characters/delete/99')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Character with ID 99 not found"
"""