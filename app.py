"""
RESTful API built using Python and Flask. It performs CRUD operations on a Python list,
which initially serves as a mock database representing characters from Game of Thrones.
The app is later migrated to use a PostgreSQL database.
"""
# Standard library imports
import os
import logging
import dotenv
# Modules installed via pip or another package manager.(Third-party imports:)
from flask import Flask, jsonify, Blueprint, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from apifairy import APIFairy, arguments, authenticate
from config.database import db, engine, Base
from config.dependancy import init_db
from models.model_tables import Character
from models.base import Base
from routers.auth import auth_blueprint, auth
from schemas.schema import (
    CharacterSchema,
    GetCharacterSchema,
    FilterCharactersQuerySchema,
    SortRequestSchema,
    UserSchema,
    UserSchemaDeletion
)

# Initialize Flask app
app = Flask(__name__)
app.name = "characters"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env file
dotenv.load_dotenv()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Access environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

# API Configuration settings
app.config['APIFAIRY_TITLE'] = 'Game of Thrones Flask API'
app.config['APIFAIRY_VERSION'] = '1.0'
app.config['APIFAIRY_UI'] = 'swagger_ui'

# Initialize APIFairy for API documentation
apifairy = APIFairy(app)

# Initialize the database
init_db(app)

# Initialize database connection with SQLAlchemy
db.init_app(app)


# Register the Blueprint for authentication
app.register_blueprint(auth_blueprint)


# Create a Blueprint with a prefix for characters
characters_blueprint = Blueprint("characters", __name__, url_prefix="/characters")



# Error Handlers
@app.errorhandler(Exception)
def handle_generic_error(e):
    logger.error(f"Unexpected Error: {str(e)}")
    return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    logger.warning(f"Validation Error: {e.messages}")
    return jsonify({"error": "Validation Error", "details": e.messages}), 400

@app.errorhandler(SQLAlchemyError)
def handle_database_error(e):
    logger.error(f"Database Error: {str(e)}")
    return jsonify({"error": "Database Error", "message": str(e)}), 500

@app.errorhandler(404)
def handle_404_error(e):
    return jsonify({"error": "Resource Not Found"}), 404

# Default home route
@app.route("/")
def home():
    """Home route of the Game of Thrones Flask API."""
    return "Welcome to the Game of Thrones Flask API!"
# Feature 1: Fetch all characters with Pagination

@characters_blueprint.route("/list-characters", methods=["GET"])
@authenticate(auth)
@arguments(CharacterSchema)
def get_characters(args):
    """Retrieve a list of characters with pagination from the Game of Thrones API."""
    try:
        limit = args.get("limit", 20)
        skip = args.get("skip", 0)
        characters = Character.query.offset(skip).limit(limit).all()
        return jsonify({
            "total": Character.query.count(),
            "skip": skip,
            "limit": limit,
            "data": [character.to_dict() for character in characters]
        })
    except Exception as e:
        return handle_generic_error(e)

# Feature 2: Fetch a specific character by ID
@characters_blueprint.route("/get-characters-id/<int:character_id>", methods=["GET"])
@authenticate(auth)
@arguments(GetCharacterSchema)
def get_character_by_id(args, character_id):
    """Retrieve a character by ID, optionally including house and role details."""
    try:
        character = Character.query.get(character_id)
        if not character:
            return jsonify({"error": "Character not found"}), 404

        result = character.to_dict()
        if args.get("include_house"):
            result["house"] = character.house
        if args.get("include_role"):
            result["role"] = character.role

        return jsonify(result)
    except Exception as e:
        return handle_generic_error(e)

# Feature 3: Fetch a filtered character list
@characters_blueprint.route("/filter-characters", methods=["GET"])
@authenticate(auth)
@arguments(FilterCharactersQuerySchema)
def filter_characters(args):
    """Filter characters based on name, house, role, and age range."""
    try:
        app.logger.info(f"Filter arguments: {args}")
        filtered_characters = Character.query

        if args.get('name'):
            filtered_characters = filtered_characters.filter(Character.name.ilike(f"%{args['name']}%"))
        if args.get('house'):
            filtered_characters = filtered_characters.filter(Character.house.ilike(f"%{args['house']}%"))
        if args.get('role'):
            filtered_characters = filtered_characters.filter(Character.role.ilike(f"%{args['role']}%"))
        if args.get('age_min'):
            filtered_characters = filtered_characters.filter(Character.age >= args['age_min'])
        if args.get('age_max'):
            filtered_characters = filtered_characters.filter(Character.age <= args['age_max'])

        filtered_characters = filtered_characters.all()

        if not filtered_characters:
            return jsonify({"total": 0, "data": []}), 200

        return jsonify({"total": len(filtered_characters), "data": [character.to_dict() for character in filtered_characters]})
    except Exception as e:
        return handle_generic_error(e)


# Feature 4: Fetch a sorted character list
@characters_blueprint.route("/characters-sort", methods=["POST"])
@authenticate(auth)
@arguments(SortRequestSchema)
def sort_characters(args):
    """Sort characters based on a specified field and order (ascending/descending)."""
    try:
        sort_key = args["sort_by"]
        reverse_order = args["sort_order"] == "desc"

        characters = Character.query.all()

        def safe_getattr(character, key):
            value = getattr(character, key, None)
            return value.lower() if isinstance(value, str) else (value or "")

        sorted_characters = sorted(
            characters,
            key=lambda x: safe_getattr(x, sort_key),
            reverse=reverse_order
        )

        return jsonify({
            "total": len(sorted_characters),
            "data": [character.to_dict() for character in sorted_characters]
        })
    except Exception as e:
        return handle_generic_error(e)

# Feature 5: Add a new character to the list
@characters_blueprint.route("/add/create-new-characters", methods=["POST"])
@authenticate(auth)
@arguments(UserSchema)
def create_character(args):
    """Create a new character and save it to the database."""
    try:
        new_character = Character(**args)
        db.session.add(new_character)
        db.session.commit()
        return jsonify(new_character.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_database_error(e)
    except Exception as e:
        return handle_generic_error(e)

# Feature 6: Edit a character
@characters_blueprint.route("/update-character/<int:character_id>", methods=["PUT"])
@authenticate(auth)
@arguments(UserSchema)
def update_character(args, character_id):
    """Update an existing character's details in the database."""
    try:
        character = Character.query.get(character_id)
        if not character:
            return jsonify({"error": f"Character with ID {character_id} not found"}), 404

        for key, value in args.items():
            if hasattr(character, key):
                setattr(character, key, value)

        db.session.commit()
        return jsonify(character.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_database_error(e)
    except Exception as e:
        return handle_generic_error(e)

# Feature 7: Delete a character
@characters_blueprint.route("/delete-characters/<int:character_id>", methods=["DELETE"])
@authenticate(auth)
@arguments(UserSchemaDeletion, location="query")
def delete_character(args, character_id):
    """Delete a character from the database by its ID."""
    try:
        character = Character.query.get(character_id)
        if not character:
            return jsonify({"error": f"Character with ID {character_id} not found"}), 404

        db.session.delete(character)
        db.session.commit()
        return jsonify({"message": f"Character with ID {character_id} deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_database_error(e)
    except Exception as e:
        return handle_generic_error(e)

# Register the Blueprint
app.register_blueprint(characters_blueprint)


# Run the app and Initialize the database before starting the app

if __name__ == "__main__":
    with app.app_context():
        Base.metadata.create_all(bind=engine)
    app.run(debug=True, host='0.0.0.0', port=8087)
