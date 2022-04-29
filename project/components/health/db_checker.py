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

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

logger = logging.getLogger(__name__)


class DBChecker:
    """Perform checks against the database."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def is_online(self) -> bool:
        """Check if database is online."""

        try:
            cursor = await self.session.execute(select(1))
            result = cursor.scalars().first()
            return result == 1
        except Exception:
            logger.exception('An exception occurred while performing database query.')

        return False
