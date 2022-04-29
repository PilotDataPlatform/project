# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from logging.config import fileConfig
from typing import Optional
from urllib.parse import urlparse

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from project.components.db_model import DBModel
from project.config import get_settings

logger = logging.getLogger('alembic')

config = context.config
fileConfig(config.config_file_name)
settings = get_settings()

target_metadata = DBModel.metadata
database_schema = config.get_main_option('database_schema', 'public')
database_uri = config.get_main_option('database_uri', settings.RDS_DB_URI)


def include_name(name: Optional[str], type_: str, parent_names: dict[str, Optional[str]]) -> bool:
    """Consider only tables from desired schema."""

    if type_ == 'schema':
        return name == database_schema

    return True


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    url = database_uri.replace(f'{urlparse(database_uri).scheme}://', 'postgresql://', 1)
    connectable = create_engine(url, poolclass=NullPool, echo=settings.RDS_ECHO_SQL_QUERIES)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=database_schema,
            include_schemas=True,
            include_name=include_name,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.execute(f'CREATE SCHEMA IF NOT EXISTS {database_schema}')
            context.run_migrations()


if context.is_offline_mode():
    logger.error('Offline migrations environment is not supported.')
    exit(1)

run_migrations_online()
