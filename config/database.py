
"""SQLAlchemy and Flask imports for database setup"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
# Standard library imports
import os



# Database URI
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sqlite_database.db'  # SQLite URI for mock database

# Initialize the SQLAlchemy engine and session maker
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SQLAlchemy()

# Base class for model definitions
Base = declarative_base()

# Initialize the database tables
def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)  # Ensure it runs at app startup

# Ensure tables are created when the application starts
init_db()
