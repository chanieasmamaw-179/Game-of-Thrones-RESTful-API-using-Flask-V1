
"""
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from config.database import db, init_db




bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
"""