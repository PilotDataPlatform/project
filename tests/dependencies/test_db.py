import pytest
from sqlalchemy.ext.asyncio import AsyncEngine

from project.config import get_settings
from project.dependencies.db import GetDBEngine


@pytest.fixture
def get_db_engine() -> GetDBEngine:
    yield GetDBEngine()


class TestGetDBEngine:
    async def test_instance_has_uninitialized_instance_attribute_after_creation(self, get_db_engine):
        assert get_db_engine.instance is None

    async def test_call_returns_an_instance_of_async_engine(self, get_db_engine):
        db_engine = await get_db_engine(settings=get_settings())
        assert db_engine is get_db_engine.instance
        assert isinstance(db_engine, AsyncEngine)
