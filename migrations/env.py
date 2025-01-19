from app import app  # Import the Flask app directly
from logging.config import fileConfig
from alembic import context

# this is the Alembic Config object, which provides access to the values
# within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Set up SQLAlchemy metadata
with app.app_context():
    config.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])

    target_metadata = app.extensions['migrate'].db.metadata

    def run_migrations_online():
        connectable = app.extensions['migrate'].db.engine
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata
            )
            with context.begin_transaction():
                context.run_migrations()

    run_migrations_online()
