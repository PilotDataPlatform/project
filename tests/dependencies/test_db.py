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
