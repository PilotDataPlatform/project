from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project.components.health.db_checker import DBChecker
from project.dependencies import get_db_session


def get_db_checker(db_session: AsyncSession = Depends(get_db_session)) -> DBChecker:
    """Return an instance of DBChecker as a dependency."""

    return DBChecker(db_session)
