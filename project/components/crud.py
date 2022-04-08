from typing import Any
from typing import Union
from uuid import UUID

from sqlalchemy.engine import CursorResult
from sqlalchemy.engine import Result
from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Executable

from project.components.db_model import DBModel
from project.components.exceptions import AlreadyExists
from project.components.exceptions import NotFound


class CRUD:
    """Base CRUD class for managing database models."""

    session: AsyncSession
    model: DBModel

    def __init__(self, db_session: AsyncSession) -> None:
        self.session = db_session
        self.transaction = None

    async def __aenter__(self) -> 'CRUD':
        """Start a new transaction."""

        self.transaction = self.session.begin()
        await self.transaction.__aenter__()

        return self

    async def __aexit__(self, *args: Any) -> None:
        """Commit an existing transaction."""

        await self.transaction.__aexit__(*args)

        return None

    async def execute(self, statement: Executable, **kwds: Any) -> Union[CursorResult, Result]:
        """Execute a statement and return buffered result."""

        return await self.session.execute(statement, **kwds)

    async def scalars(self, statement: Executable, **kwds: Any) -> ScalarResult:
        """Execute a statement and return scalar result."""

        return await self.session.scalars(statement, **kwds)

    async def create_one(self, statement: Executable) -> Union[UUID, str]:
        """Execute a statement to create one entry."""

        try:
            result = await self.execute(statement)
        except IntegrityError:
            raise AlreadyExists()

        return result.inserted_primary_key.id

    async def retrieve_one(self, statement: Executable) -> DBModel:
        """Execute a statement to retrieve one entry."""

        result = await self.scalars(statement)
        instance = result.first()

        if instance is None:
            raise NotFound()

        return instance

    async def retrieve_many(self, statement: Executable) -> list[DBModel]:
        """Execute a statement to retrieve multiple entries."""

        result = await self.scalars(statement)
        instances = result.all()

        return instances

    async def update_one(self, statement: Executable) -> None:
        """Execute a statement to update one entry."""

        result = await self.execute(statement)

        if result.rowcount == 0:
            raise NotFound()

    async def delete_one(self, statement: Executable) -> None:
        """Execute a statement to delete one entry."""

        result = await self.execute(statement)

        if result.rowcount == 0:
            raise NotFound()
