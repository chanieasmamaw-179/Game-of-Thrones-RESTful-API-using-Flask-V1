from alembic.env import config
from app import app, db  # Make sure to import your Flask app and db
from alembic import context
from logging.config import fileConfig

# This imports the Flask app and database instance
app = app()  # or however you initialize your app

# Ensure Flask app context is available
with app.app_context():
    # Load the configuration from the app (this makes sure we use the right DB URL)
    fileConfig(config.get_main_option("config_file"))

    # Now, we can use Alembic commands that need the app context
    target_metadata = db.metadata
    # Other Alembic setup here
