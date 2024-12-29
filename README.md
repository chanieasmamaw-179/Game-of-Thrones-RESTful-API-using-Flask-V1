Flask Game of Thrones API

This project is a Flask-based RESTful API designed to manage and retrieve information about characters from the fictional world of Game of Thrones. It features endpoints for listing, filtering, sorting, creating, updating, and deleting character records.
Features

    Fetch All Characters with Pagination
    Retrieve a paginated list of all characters.
    Endpoint: /list-characters
    Method: GET

    Fetch Character by ID
    Retrieve detailed information about a specific character.
    Endpoint: /get-characters-id/<int:character_id>
    Method: GET

    Filter Characters
    Retrieve a filtered list of characters based on query parameters (e.g., name, house, role, age range).
    Endpoint: /filter-characters
    Method: GET

    Sort Characters
    Sort characters by name, age, or house in ascending or descending order.
    Endpoint: /characters-sort
    Method: POST

    Filter and Sort Combined
    Combine filtering and sorting functionality in one request.
    Endpoint: /characters-filter-and-sort-combin
    Method: POST

    Add a New Character
    Create a new character record with a unique ID.
    Endpoint: /add/create-new-characters
    Method: POST

    Update an Existing Character
    Modify the details of an existing character by ID.
    Endpoint: /Edit-characters/<int:character_id>
    Method: PUT

    Delete a Character
    Remove a character record by ID.
    Endpoint: /delete-characters/<int:character_id>
    Method: DELETE

Installation and Setup

    Clone the Repository:

git clone <repository_url>
cd flask_got_api

Set Up Virtual Environment:

python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install Dependencies:

pip install -r requirements.txt

Run the Application:

    python app.py

    The application will be accessible at http://localhost:8087.

API Documentation
Query Parameters

    limit: Number of results per page (default: 20).
    skip: Number of results to skip (default: 0).

Request Body Parameters

Create/Update Character

{
    "name": "string",
    "house": "string",
    "role": "string",
    "age": "integer"
}

Filter Parameters

{
    "name": "string",
    "house": "string",
    "role": "string",
    "age_min": "integer",
    "age_max": "integer",
    "sort_by": "string",
    "sort_order": "asc|desc"
}

Development Tools
Dependencies

    Flask: Python web framework.
    APIFairy: API documentation generation.
    Marshmallow: Input validation.
    Flask-SQLAlchemy: SQLAlchemy integration for Flask.
    Flask-Swagger-UI: API UI for Swagger.
    passlib: Password hashing.
    PyJWT: JSON Web Token (JWT) authentication.
    psycopg2-binary: PostgreSQL database adapter.
    pydantic: Data validation.
    python-dotenv: Load environment variables from a .env file.

Configuration

    Debugging is enabled in development mode.
    API UI is available at /swagger-ui.

Database

This application uses PostgreSQL as its database.
License

This project is licensed under the webeet.io. License.
Author

Asmamaw Chanie Yehun
Junior Backend Software Engineer
Email: chanieasmamaw@yahoo.com
Phone: +4917625315666
