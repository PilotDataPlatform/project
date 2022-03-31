from unittest.mock import Mock

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

from project.config import get_settings
from project.dependencies.db import GetDBEngine
from project.dependencies.db import GetDBSession


@pytest.fixture
def get_db_engine() -> GetDBEngine:
    yield GetDBEngine()


@pytest.fixture
def get_db_session() -> GetDBSession:
    yield GetDBSession()


class TestGetDBEngine:
    async def test_instance_has_uninitialized_instance_attribute_after_creation(self, get_db_engine):
        assert get_db_engine.instance is None

    async def test_call_returns_an_instance_of_async_engine(self, get_db_engine):
        db_engine = await get_db_engine(settings=get_settings())
        assert db_engine is get_db_engine.instance
        assert isinstance(db_engine, AsyncEngine)


class TestGetDBSession:
    async def test_instance_has_uninitialized_instance_attribute_after_creation(self, get_db_session):
        assert get_db_session.instance is None

    async def test_call_returns_each_time_a_new_instance_of_async_session(self, get_db_session):
        engine = Mock()
        db_session_1 = await get_db_session(engine=engine)
        db_session_2 = await get_db_session(engine=engine)

        assert isinstance(db_session_1, AsyncSession)
        assert isinstance(db_session_2, AsyncSession)
        assert db_session_1 is not db_session_2
