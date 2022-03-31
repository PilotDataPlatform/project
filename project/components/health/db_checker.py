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
