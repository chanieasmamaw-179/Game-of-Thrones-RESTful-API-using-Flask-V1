Game of Thrones Flask API
Overview

This project is a RESTful API built using Python and Flask that performs CRUD operations on a list of characters from the Game of Thrones universe. Initially, a mock database represented by a Python list was used, but the app has now been migrated to use a PostgreSQL database. The API provides several functionalities, including listing characters with pagination, retrieving specific character details, and filtering or sorting characters based on various criteria.
Features

    Fetch all characters with Pagination
    Endpoint: GET /list-characters
    Supports pagination and returns a list of characters.

    Fetch a specific character by ID
    Endpoint: GET /get-characters-id/<int:character_id>
    Retrieves details of a character by their ID, with optional inclusion of house and role.

    Filter characters by name, house, role, or age range
    Endpoint: GET /filter-characters
    Allows filtering of characters based on various attributes like name, house, role, and age range.

    Sort characters by a specified field
    Endpoint: POST /characters-sort
    Sorts characters based on a specific field (e.g., name, age) in either ascending or descending order.

    Create a new character
    Endpoint: POST /add/create-new-characters
    Allows adding new characters to the database.

    Update an existing character
    Endpoint: PUT /update-character/<int:character_id>
    Allows updating the details of an existing character by their ID.

    Delete a character by ID
    Endpoint: DELETE /delete-characters/<int:character_id>
    Deletes a character from the database by their ID.

Requirements

To set up and run this API, you need to install the following Python packages:
---------------------------------------------------------------------------------------------------------
Flask>=3.0.0  
flask_migrate  
flask-restful  
flask-paginate  
SQLAlchemy  
psycopg2-binary  
requests  
jsonify  
pydantic  
sqlalchemy  
flask_sqlalchemy  
flask-swagger-ui  
mysqlclient  
python-dotenv  
apifairy==0.9.0  
passlib  
PyJWT  
pymysql  
alembic  
python-dotenv  
marshmallow-sqlalchemy  
flask_restx  
Authlib  
flask-bcrypt  
flask_jwt_extended  
pytest  
pytest-cov  
pytest-xdist
---------------------------------------------------------------------------------------------------------
1. Installation and Setup

    Clone the repository
    Clone the repository to your local machine:
git clone https://github.com/chanieasmamaw-179/Game-of-Thrones-RESTful-API-using-Flask-V1
cd https://github.com/chanieasmamaw-179/Game-of-Thrones-RESTful-API-using-Flask-V1

2. Install dependencies
Install the required dependencies from the requirements.txt file:
pip install -r requirements.txt

3. Set up environment variables
Create a .env file in the root of the project directory and configure the following variables: 

DATABASE_URL=your_database_connection_string
FLASK_APP=app.py
FLASK_ENV=development
4. Run the Flask app
To start the Flask application, run the following command:
python app.py
The app will be available at http://localhost:8087.

## Testing Setup

To run tests, install pytest and other testing dependencies by running:
- pip install pytest pytest-cov pytest-xdist

Running Tests:

To run the tests, execute the following command:
pytest
    To see test coverage, use:
- pytest --cov=app
or
-  pytest --cov=app -v --disable-warnings   # it removes the warning isues

You can also specify a particular test file to run:

- pytest test_app.py

## API Documentation

The API provides interactive documentation via Swagger UI. After running the app, you can access the documentation at:
http://192.168.171.163:8087/docs#


## Database Setup

This app uses PostgreSQL as its database. To set up the database:

    Ensure that you have PostgreSQL installed and running.
    Configure your PostgreSQL database connection URL in the .env file.
    Run database migrations to set up the schema:
- flask db upgrade
## Error Handling

The application handles different types of errors gracefully:

    500 Internal Server Error: A generic error handler for unexpected issues.
    400 Bad Request: Validation errors are returned with details.
    404 Not Found: Returned if the requested character does not exist.

## Folder Structure
The folder structure of the project is as follows:
------------------------------------------------------------------------------------------------------
app/
│-- __init__.py
│-- app.py                   # Main application file
│-- config/
│   ├-- database.py          # Database configuration
│   └-- dependancy.py        # Database initialization and app configurations
│-- models/
│   ├-- __init__.py
│   ├-- model_tables.py      # Models (e.g., Character)
│   └-- base.py              # Base model class for SQLAlchemy
│-- routers/
│   └-- auth.py              # Authentication routes
│-- schemas/
│   └-- schema.py            # Marshmallow schemas for data validation
│-- test_app.py              # Unit tests
│-- requirements.txt         # Project dependencies
│-- .env                     # Environment variables
------------------------------------------------------------------------------------------------------

License

This project is licensed under the webeet.io Job Application Mock Interview.

Author: Asmamaw Chanie Yehun, PhD, Backend Software Developer
Email: chanieasmamaw@yahoo.com
Phone: +49 176 25315666
