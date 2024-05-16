import asyncio
from logging.config import fileConfig
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from app.feats.models import *  # noqa
from app.settings import settings
from app.core.database import Base


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
section = config.config_ini_section
config.set_section_option(section, "DB_PROVIDER", str(settings.database.provider))
config.set_section_option(section, "DB_USER", str(settings.database.user))
config.set_section_option(section, "DB_PASSWORD", str(settings.database.password))
config.set_section_option(section, "DB_HOST", str(settings.database.host))
config.set_section_option(section, "DB_PORT", str(settings.database.port))
config.set_section_option(section, "DB_NAME", str(settings.database.database))


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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
