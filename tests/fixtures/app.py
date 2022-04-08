import asyncio
from asyncio import AbstractEventLoop
from contextlib import AbstractContextManager
from typing import Any
from typing import Callable

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from project.app import create_app
from project.config import Settings
from project.config import get_settings


class OverrideDependencies(AbstractContextManager):
    """Temporarily override application dependencies using context manager."""

    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.stashed_dependencies = {}
        self.dependencies_to_override = {}

    def __call__(self, dependencies: dict[Callable[..., Any], Callable[..., Any]]) -> 'OverrideDependencies':
        self.dependencies_to_override = dependencies
        return self

    def __enter__(self) -> 'OverrideDependencies':
        self.stashed_dependencies = self.app.dependency_overrides.copy()
        self.app.dependency_overrides.update(self.dependencies_to_override)
        return self

    def __exit__(self, *args: Any) -> None:
        self.app.dependency_overrides.clear()
        self.app.dependency_overrides.update(self.stashed_dependencies)
        self.dependencies_to_override = {}
        return None


@pytest.fixture
def override_dependencies(app) -> OverrideDependencies:
    yield OverrideDependencies(app)


@pytest.fixture(scope='session')
def event_loop() -> AbstractEventLoop:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def settings(database_uri) -> Settings:
    settings = Settings(RDS_DB_URI=database_uri)
    yield settings


@pytest.fixture
def app(event_loop, settings) -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    yield app


@pytest.fixture
async def client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url='https://') as client:
        yield client
