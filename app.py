
from flask import Flask, jsonify, Blueprint
from flask_migrate import Migrate
from apifairy import APIFairy, arguments
from config.database import db, engine, Base
from config.dependancy import init_db
from models.model_tables import Character
from models.base import Base
from routers.auth import auth_blueprint
from schemas.schema import CharacterSchema, GetCharacterSchema, FilterCharactersQuerySchema, SortRequestSchema, \
    UserSchema, UserSchemaDeletion
from marshmallow import Schema, fields, ValidationError
import os
import dotenv



# Initialize Flask app
app = Flask(__name__)

# Load .env file
dotenv.load_dotenv()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Access environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///./sqlite_database.db')   # Make sure DATABASE_URL is correctly loaded
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

# Default home route
@app.route("/")
def home():
    return "Welcome to the Game of Thrones Flask API!"

# Feature 1: Fetch all characters with Pagination
@app.route("/list-characters", methods=["GET"])
@arguments(CharacterSchema)
def get_characters(args):
    limit = args.get("limit", 20)
    skip = args.get("skip", 0)

    characters = Character.query.offset(skip).limit(limit).all()

    return jsonify({
        "total": Character.query.count(),
        "skip": skip,
        "limit": limit,
        "data": [character.to_dict() for character in characters]
    })

# Feature 2: Fetch a specific character by ID
@app.route("/get-characters-id/<int:character_id>", methods=["GET"])
@arguments(GetCharacterSchema)
def get_character_by_id(args, character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    result = character.to_dict()
    if args["include_house"]:
        result["house"] = character.house
    if args["include_role"]:
        result["role"] = character.role

    return jsonify(result)

# Feature 3: Fetch a filtered character list
@app.route("/filter-characters", methods=["GET"])
@arguments(FilterCharactersQuerySchema)
def filter_characters(args):
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
        return jsonify({"error": "No characters found matching the given filters."}), 404

    return jsonify({"total": len(filtered_characters), "data": [character.to_dict() for character in filtered_characters]})

# Feature 4: Fetch a sorted character list
@app.route("/characters-sort", methods=["POST"])
@arguments(SortRequestSchema)
def sort_characters(args):
    sort_key = args["sort_by"]
    reverse_order = args["sort_order"] == "desc"

    characters = Character.query.all()

    # Define a function for safe attribute access and handling None values
    def safe_getattr(character, key):
        value = getattr(character, key)
        if isinstance(value, str):
            return value.lower() if value is not None else ""  # Default to empty string if None
        return value if value is not None else ""  # Default to empty string if None for non-string types

    sorted_characters = sorted(
        characters,
        key=lambda x: safe_getattr(x, sort_key),  # Use safe_getattr for comparison
        reverse=reverse_order
    )

    return jsonify({
        "total": len(sorted_characters),
        "data": [character.to_dict() for character in sorted_characters]
    })


# Feature 5: Add a new character to the list
@app.route("/add/create-new-characters", methods=["POST"])
@arguments(UserSchema)
def create_character(args):
    print("Incoming JSON data:", args)  # Log parsed arguments
    new_character = Character(**args)
    db.session.add(new_character)
    db.session.commit()

    print("Saved character:", new_character.to_dict())  # Log the saved character
    return jsonify(new_character.to_dict()), 201

# Feature 6: Edit a character
@app.route("/update-character/<int:character_id>", methods=["PUT"])
@arguments(UserSchema)
def update_character(args, character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": f"Character with ID {character_id} not found"}), 404

    for key, value in args.items():
        if hasattr(character, key):
            setattr(character, key, value)

    db.session.commit()
    return jsonify(character.to_dict()), 200

# Feature 7: Delete a character
@app.route("/delete-characters/<int:character_id>", methods=["DELETE"])
@arguments(UserSchemaDeletion, location="query") #if I use this argument , add "arg" in side function
def delete_character(arg,  character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": f"Character with ID {character_id} not found"}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({"message": f"Character with ID {character_id} deleted successfully"}), 200

# Run the app and Initialize the database before starting the app
if __name__ == "__main__":
    with app.app_context():
        Base.metadata.create_all(bind=engine)  # Ensure tables are created
    app.run(debug=True, host='0.0.0.0', port=8087)