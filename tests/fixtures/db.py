import os
from contextlib import contextmanager
from pathlib import Path

import pytest
from alembic.command import upgrade
from alembic.config import Config
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

    return path


@pytest.fixture(scope='session')
def database_uri(project_root) -> str:
    with PostgresContainer(POSTGRES_DOCKER_IMAGE) as pg_container:
        database_uri = pg_container.get_connection_url()

        config = Config('migrations/alembic.ini')
        with chdir(project_root):
            config.set_main_option('database_uri', database_uri)
            upgrade(config, 'head')

        yield database_uri
