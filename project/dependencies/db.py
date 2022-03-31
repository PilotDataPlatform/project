from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from project.config import Settings
from project.config import get_settings


class GetDBEngine:
    """Create a FastAPI callable dependency for SQLAlchemy single AsyncEngine instance."""

    def __init__(self) -> None:
        self.instance = None

    async def __call__(self, settings: Settings = Depends(get_settings)) -> AsyncEngine:
        """Return an instance of AsyncEngine class."""

        if not self.instance:
            self.instance = create_async_engine(settings.RDS_DB_URI)
        return self.instance


get_db_engine = GetDBEngine()


class GetDBSession:
    """Create a FastAPI callable dependency for SQLAlchemy AsyncSession instance."""

    def __init__(self) -> None:
        self.instance = None

    async def __call__(self, engine: AsyncEngine = Depends(get_db_engine)) -> AsyncSession:
        """Return an instance of AsyncSession class."""

        if not self.instance:
            self.instance = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

        async with self.instance() as session:
            return session


get_db_session = GetDBSession()
