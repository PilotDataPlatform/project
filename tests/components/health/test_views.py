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

from unittest.mock import AsyncMock
from unittest.mock import Mock

from sqlalchemy.exc import SQLAlchemyError

from project.components.health.db_checker import DBChecker
from project.components.health.dependencies import get_db_checker


class TestHealthViews:
    async def test_health_endpoint_returns_204_when_db_is_live(self, client):
        response = await client.get('/v1/health/')

        assert response.status_code == 204

    async def test_health_endpoint_returns_503_when_db_is_not_live(self, client, override_dependencies):
        def db_checker():
            session = Mock()
            session.execute = AsyncMock(side_effect=SQLAlchemyError)
            return DBChecker(session)

        with override_dependencies({get_db_checker: db_checker}):
            response = await client.get('/v1/health/')

        assert response.status_code == 503
