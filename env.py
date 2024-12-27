from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config

connectable = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)
