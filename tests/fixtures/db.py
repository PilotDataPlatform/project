import pytest
from testcontainers.postgres import PostgresContainer

POSTGRES_DOCKER_IMAGE = 'postgres:14.2-alpine'


@pytest.fixture(scope='session')
def db_uri():
    with PostgresContainer(POSTGRES_DOCKER_IMAGE) as pg_container:
        db_uri = pg_container.get_connection_url()
        yield db_uri
