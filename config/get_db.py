from flask import Flask, jsonify
from sqlalchemy.orm import Session
from config.database import Base, engine
from models.model_tables import Character
from config.dependancy import get_db




app = Flask(__name__)

@app.route("/get-characters", methods=["GET"])
def get_characters():
    """
    Fetch characters from the database.
    """
    db: Session = get_db()  # Get the database session
    characters = db.query(Character).all()  # Query the database
    return jsonify([character.to_dict() for character in characters])

