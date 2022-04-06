import logging
from logging.config import fileConfig
from typing import Dict
from typing import Optional
from urllib.parse import urlparse

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy.pool import NullPool

from project.components.db_model import DBModel
from project.config import get_settings

logger = logging.getLogger('alembic')

settings = get_settings()
db_uri = settings.RDS_DB_URI.replace(f'{urlparse(settings.RDS_DB_URI).scheme}://', 'postgresql://', 1)
db_schema = 'project'
target_metadata = DBModel.metadata

config = context.config
fileConfig(config.config_file_name)
config.set_main_option('sqlalchemy.url', db_uri)


def include_name(name: Optional[str], type_: str, parent_names: Dict[str, Optional[str]]) -> bool:
    """Consider only tables from desired schema."""

    if type_ == 'schema':
        return name == db_schema

    return True


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    connectable = engine_from_config(config.get_section(config.config_ini_section), poolclass=NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=db_schema,
            include_schemas=True,
            include_name=include_name,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    logger.error('Offline migrations environment is not supported.')
    exit(1)

run_migrations_online()
