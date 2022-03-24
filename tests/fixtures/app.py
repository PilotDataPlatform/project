import asyncio

import pytest
from httpx import AsyncClient

from project.app import create_app


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def app(event_loop):
    app = create_app()
    yield app


@pytest.fixture
async def client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url='https://') as client:
        yield client
