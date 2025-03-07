"""Test setup and import required modules for the application."""
# Import necessary modules and libraries
import pytest
import werkzeug
from importlib.metadata import version
#Local Application Imports
from app import app, db
from models.model_tables import Character



if not hasattr(werkzeug, "__version__"):
    """Check and set the version of werkzeug if it's not already set."""
    werkzeug.__version__ = version("werkzeug")


@pytest.fixture(scope='module')
def test_client():
    """Fixture to set up the test client and configure the app for testing."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://game_of_thrones_flask_api_1_0_user:gFBXaYrJKJHbYogg7YcAzML15pQFrQOH@dpg-ctli3udds78s73c70dd0-a.frankfurt-postgres.render.com/game_of_thrones_flask_api_1_0'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()

    with app.test_client() as testing_client:
        yield testing_client

    with app.app_context():
        db.session.remove()


@pytest.fixture(scope='function')
def test_init_database():
    """Fixture to initialize the database with a sample character for each test."""
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


def test_home_route(test_client):
    """Test the home route to ensure it returns the correct status and message."""
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Game of Thrones Flask API!" in response.data


# Test for Feature 1 listing characters and pagination----Done
def test_get_characters_with_pagination(test_client):
    """Test the GET /list-characters endpoint with pagination to ensure correct data retrieval."""
    # Query initial database state
    initial_total = Character.query.count()

    # For this test data must exist in the database
    test_characters = [
        {"name": "Jon Snow" , "house": "Stark","animal":"Direwolf","symbol":"Wolf","nickname":"King in the North","role":"King","age":25,"death":8,"strength":"Physically strong"}
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


# Test for  Feature 2 fetching a specific character by ID ----- Done
def test_get_character_by_id(test_client, test_init_database):
    """Test the GET /get-characters-id/{id} endpoint with various scenarios."""
    response = test_client.get('/get-characters-id/1?include_house=true&include_role=true')
    assert response.status_code == 200

    # Test with missing parameters (should not include house and role)
    response = test_client.get('/get-characters-id/1')
    assert response.status_code == 200


    # Test with invalid ID (non-existent character)
    response = test_client.get('/get-characters-id/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Character not found"


# Test for Feature 3 fetching filtered characters --- done in API endpoints but test is flied!!
def test_filter_characters(test_client, test_init_database):
    """Test the filtering functionality of the GET /filter-characters endpoint."""

    # Clean up the database to avoid duplicates before adding the test character
    Character.query.filter_by(name="Bran Stark").delete()
    db.session.commit()

    # Seed the database with a single character
    character = Character(
        name="Bran Stark",
        house="Stark",
        animal="",
        symbol="Raven",
        nickname="Three-Eyed Raven",
        role="Seer",
        age=20,
        death=0,
        strength="Mystical"
    )
    db.session.add(character)
    db.session.commit()

    # Test filtering by name
    response = test_client.get('/filter-characters?name=Bran%20Stark')

    # Debugging: Print the response if necessary
    print(f"Response: {response.json if response.status_code == 200 else response.data.decode()}")

    # Assert the response status code
    assert response.status_code == 200

    # Assert the total number of filtered characters is 1 (now that duplicates are removed)
    assert response.json["total"] == 1

    # Assert the character's role is correctly set to "Seer"
    assert response.json["data"][0]["role"] == "Seer"


# Test sorting characters for feature 4 by name, age and other options in ascending or descending order
def test_sort_characters_by_name_ascending(test_client, test_init_database):
    """Test the sorting functionality of the /characters-sort endpoint by character name in ascending order."""

    payload = {"sort_by": "name", "sort_order": "asc"}
    response = test_client.post("/characters-sort", json=payload)
    assert response.status_code == 200


# Test for sorting characters by age (descending)
def test_sort_characters_by_age_descending(test_client, test_init_database):
    """Test the sorting functionality of the /characters-sort endpoint by character age in descending order."""
    payload = {"sort_by": "age", "sort_order": "desc"}
    response = test_client.post("/characters-sort", json=payload)
    assert response.status_code == 200

def test_create_character(test_client):
    """Test the creation of a new character through the /add/create-new-characters endpoint."""
    query_params = {
        "name": "Asmamaw Y",
        "house": "Stark",
        "animal": "",
        "symbol": "Lizard-lion",
        "nickname": "",
        "role": "Lizard-lion",
        "age": 16,
        "death": 4,
        "strength": "Visionary"
    }
    response = test_client.post('/add/create-new-characters', query_string=query_params)

    assert response.status_code == 201
    assert response.json['name'] == 'Asmamaw Y'
    assert response.json['house'] == 'Stark'
    assert response.json['symbol'] == 'Lizard-lion'
    assert response.json['role'] == 'Lizard-lion'


# Test for editing a character Feature 6 -- done
def test_edit_character(test_client, test_init_database):
    """Test the editing of an existing character through the /update-character/{id} endpoint."""

    response = test_client.put('/update-character/11')
    assert response.status_code == 200
    response_data = response.get_json()
    response.status_code = response_data["id"]="11"


# Test for removing a character Feature 7 --- done
def test_delete_character(test_client, test_init_database):
    """Test the deletion of a character through the /delete-characters/{id} endpoint."""
    response = test_client.delete('/delete-characters/11')
    print(response)

