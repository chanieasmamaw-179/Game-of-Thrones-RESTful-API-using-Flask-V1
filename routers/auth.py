import logging
import os
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from apifairy import arguments
from passlib.context import CryptContext
import jwt
from sqlalchemy.exc import IntegrityError
from config.database import db
from schemas.schema import RegisterSchema, TokenResponseSchema
from schemas.user import User

# Blueprint Initialization
auth_blueprint = Blueprint('auth', __name__)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 180))

# Security settings
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@auth_blueprint.route('/auth/register', methods=['POST'])
@arguments(RegisterSchema)
def register_user(args):
    try:
        if args["password"] != args["confirm_password"]:
            return jsonify({"error": "Passwords do not match"}), 400

        hashed_password = bcrypt_context.hash(args["password"])
        new_user = User(name=args["name"], email=args["email"], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email is already registered"}), 400
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@auth_blueprint.route("/auth/token", methods=["POST"])
@arguments(TokenResponseSchema)
def login(args):
    user = User.query.filter_by(email=args["email"]).first()

    if not user or not bcrypt_context.verify(args["password"], user.password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token({"sub": user.id})
    return jsonify({"access_token": access_token, "token_type": "bearer"}), 200