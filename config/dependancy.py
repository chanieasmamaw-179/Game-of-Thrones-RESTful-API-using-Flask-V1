"""Logging setup and Flask database session management."""
import logging
from flask import g

# SQLAlchemy imports for session management
from sqlalchemy.orm import Session

# Local database session import from the configuration
from config.database import SessionLocal



# Initialize logger
logger = logging.getLogger(__name__)

def get_db():
    """
    Provides a database session for Flask.
    The session is tied to the current request.
    """
    if "db" not in g:
        try:
            # Create a new session if it doesn't exist in `g`
            g.db = SessionLocal()
        except Exception as e:
            logger.error("Error connecting to the database: %s", str(e))
            raise Exception("Database connection error")

    return g.db

def close_db(error=None):
    """
    Closes the database session when the request ends.
    Rolls back the transaction if there was an error.
    """
    db = getattr(g, "db", None)
    if db is not None:
        try:
            if error:
                db.rollback()  # Roll back any pending transaction in case of an error
            db.close()
        except Exception as e:
            logger.error("Error closing the database session: %s", str(e))

def init_db(app):
    """
    Initializes the Flask app with database session handling.
    Registers the database cleanup function on request teardown.
    """
    app.teardown_appcontext(close_db)
