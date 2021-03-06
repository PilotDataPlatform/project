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

import os
from contextlib import contextmanager
from pathlib import Path

import pytest
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from testcontainers.postgres import PostgresContainer

POSTGRES_DOCKER_IMAGE = 'postgres:14.2-alpine'


@contextmanager
def chdir(directory: Path) -> None:
    cwd = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cwd)


@pytest.fixture(scope='session')
def project_root() -> Path:
    path = Path(__file__)

    while path.name != 'project':
        path = path.parent

    yield path


@pytest.fixture(scope='session')
def db_uri(project_root) -> str:
    with PostgresContainer(POSTGRES_DOCKER_IMAGE) as pg_container:
        database_uri = pg_container.get_connection_url()

        config = Config('migrations/alembic.ini')
        with chdir(project_root):
            config.set_main_option('database_uri', database_uri)
            upgrade(config, 'head')

        yield database_uri


@pytest.fixture(scope='session')
def db_engine(settings) -> AsyncEngine:
    yield create_async_engine(settings.RDS_DB_URI, echo=settings.RDS_ECHO_SQL_QUERIES)


@pytest.fixture
async def db_session(db_engine) -> AsyncSession:
    session = AsyncSession(bind=db_engine, expire_on_commit=False)

    try:
        yield session
    finally:
        await session.close()
