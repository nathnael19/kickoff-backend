from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel
from app.core.config import settings  # your DBSettings
from app.model.models import (
    Team,
    Card,
    Goal,
    Match,
    MatchEvent,
    Player,
    Standing,
    MatchLineup,
    Tournament,
)  # import all models here

# Alembic Config object
config = context.config

# Override sqlalchemy.url with your settings
config.set_main_option("sqlalchemy.url", settings.postgres_url)

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Link your models for autogenerate
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
