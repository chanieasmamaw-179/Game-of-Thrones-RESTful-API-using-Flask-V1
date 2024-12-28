import pytest
import werkzeug
from importlib.metadata import version
from app import app, db
from models.model_tables import Character

if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = version("werkzeug")

# Fixture for setting up the test client
# Fixture for setting up the test client
@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://game_of_thrones_flask_api_1_0_user:gFBXaYrJKJHbYogg7YcAzML15pQFrQOH@dpg-ctli3udds78s73c70dd0-a.frankfurt-postgres.render.com/game_of_thrones_flask_api_1_0'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()

    with app.test_client() as testing_client:
        yield testing_client

    with app.app_context():
        db.session.remove()


# Fixture for initializing sample data
@pytest.fixture(scope='function')
def test_init_database():
    # Initialize the database with a sample character
    test_character = Character(
        name="Bran Stark",
        house="Stark",
        animal="Raven",
        symbol="Three-Eyed Raven",
        nickname="king kong",
        role="King",
        age=25,
        death=0,
        strength="Physically strong"
    )
    #db.session.add(test_character)
    #db.session.commit()

    # Yield to run the test
    yield

    # Clean up after each test function (delete the test character)
    #db.session.query(Character).filter_by(name="Bran Stark").delete()
    db.session.commit()

# Test for the home route
def test_home_route(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Game of Thrones Flask API!" in response.data


# Test for listing characters and pagination
def test_get_characters_with_pagination(test_client):
    # Query initial database state
    initial_total = Character.query.count()

    # For this test data must exist in the database
    test_characters = [
        {"name": "Bran Stark", "house": "Stark","animal":"Raven","symbol":"Three-Eyed Raven","nickname":"king kong","role":"King","age":"25","death":"0","strength":"Physically strong"}
    ]
    existing_names = {char.name for char in Character.query.all()}

    for char in test_characters:
        if char["name"] not in existing_names:
            db.session.add(Character(**char))
    db.session.commit()

    # Calculate the expected total after adding new test data
    expected_total = initial_total + len(
        [char for char in test_characters if char["name"] not in existing_names]
    )

    # Call the endpoint
    response = test_client.get('/list-characters?limit=1')
    assert response.status_code == 200
    data = response.get_json()

    # Assertions
    assert data["total"] == expected_total, f"Expected {expected_total}, got {data['total']}"
    assert len(data["data"]) == 1  # Pagination limit is 1
    assert data["data"][0]["name"] in [char["name"] for char in test_characters]


# Test for fetching a specific character by ID
def test_get_character_by_id(test_client, test_init_database):
    # Test with valid ID and query parameters (including house and role)
    response = test_client.get('/get-characters-id/74?include_house=true&include_role=true')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Bran Stark"
    assert data["role"] == "King"

    # Test with missing parameters (should not include house and role)
    response = test_client.get('/get-characters-id/74')
    assert response.status_code == 200


    # Test with invalid ID (non-existent character)
    response = test_client.get('/get-characters-id/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Character not found"


"""

# Test for fetching filtered characters
def test_filter_characters(test_client, test_init_database):
    print(test_client)
    print(test_init_database)
    print(test_filter_characters)
    # Test filtering by name
    response = test_client.get('/filter-characters/?name=Bran Stark')
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["data"][0]["name"] == "Bran Stark"

"""

# Test for adding a character
def test_create_character(test_client):
    response = test_client.post('/add/create-new-characters')
    assert response.status_code == 201
    #assert response.json['id'] == 89

# Test for editing a character
def test_edit_character(test_client, test_init_database):
    updated_data = {
        "id": 80,
        "name": "Bran Stark",
        "age": 25
    }
    response = test_client.put('/update-character/80', json=updated_data)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["name"] == "Bran Stark"
    assert response_data["age"] == 25


# Test for removing a character
def test_delete_character(test_client, test_init_database):

    # Test deleting the character
    response = test_client.delete('/delete-characters/86')
    print(response)
    #assert response.status_code == 200
