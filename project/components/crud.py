from typing import Any
from typing import Union
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.engine import CursorResult
from sqlalchemy.engine import Result
from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import Executable

from project.components.db_model import DBModel
from project.components.exceptions import AlreadyExists
from project.components.exceptions import NotFound
from project.components.pagination import Page
from project.components.pagination import Pagination
from project.components.schemas import BaseSchema


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

    async def _create_one(self, statement: Executable) -> Union[UUID, str]:
        """Execute a statement to create one entry."""

        try:
            result = await self.execute(statement)
        except IntegrityError:
            raise AlreadyExists()

        return result.inserted_primary_key.id

    async def _retrieve_one(self, statement: Executable) -> DBModel:
        """Execute a statement to retrieve one entry."""

        result = await self.scalars(statement)
        instance = result.first()

        if instance is None:
            raise NotFound()

        return instance

    async def _retrieve_many(self, statement: Executable) -> list[DBModel]:
        """Execute a statement to retrieve multiple entries."""

        result = await self.scalars(statement)
        instances = result.all()

        return instances

    async def _update_one(self, statement: Executable) -> None:
        """Execute a statement to update one entry."""

        result = await self.execute(statement)

        if result.rowcount == 0:
            raise NotFound()

    async def _delete_one(self, statement: Executable) -> None:
        """Execute a statement to delete one entry."""

        result = await self.execute(statement)

        if result.rowcount == 0:
            raise NotFound()

    async def create(self, entry_create: BaseSchema) -> DBModel:
        """Create a new entry."""

        values = entry_create.dict()
        statement = insert(self.model).values(**values)
        entry_id = await self._create_one(statement)

        entry = await self.retrieve_by_id(entry_id)

        return entry

    async def retrieve_by_id(self, id_: UUID) -> DBModel:
        """Get an existing entry by id (primary key)."""

        statement = select(self.model).where(self.model.id == id_)
        entry = await self._retrieve_one(statement)

        return entry

    async def list(self) -> list[DBModel]:
        """Get all existing entries."""

        statement = select(self.model)
        entries = await self._retrieve_many(statement)

        return entries

    async def paginate(self, pagination: Pagination) -> Page:
        """Get all existing entries with pagination support."""

        statement = select(func.count()).select_from(self.model)
        count = await self._retrieve_one(statement)

        statement = select(self.model).limit(pagination.limit).offset(pagination.offset)
        entries = await self._retrieve_many(statement)

        return Page(pagination=pagination, count=count, entries=entries)

    async def update(self, id_: UUID, entry_update: BaseSchema) -> DBModel:
        """Update an existing entry attributes."""

        values = entry_update.dict(exclude_unset=True, exclude_defaults=True)
        statement = update(self.model).where(self.model.id == id_).values(**values)
        await self._update_one(statement)

        entry = await self.retrieve_by_id(id_)

        return entry

    async def delete(self, id_: UUID) -> None:
        """Remove an existing entry."""

        statement = delete(self.model).where(self.model.id == id_)

        await self._delete_one(statement)
