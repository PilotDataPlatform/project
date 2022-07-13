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

from typing import Any
from typing import Optional
from typing import Type
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
from project.components.filtering import Filtering
from project.components.pagination import Page
from project.components.pagination import Pagination
from project.components.schemas import BaseSchema
from project.components.sorting import Sorting


class CRUD:
    """Base CRUD class for managing database models."""

    session: AsyncSession
    model: Type[DBModel]

    def __init__(self, db_session: AsyncSession) -> None:
        self.session = db_session
        self.transaction = None

    async def __aenter__(self) -> 'CRUD':
        """Start a new transaction."""

        self.transaction = self.session.begin_nested()
        await self.transaction.__aenter__()

        return self

    async def __aexit__(self, *args: Any) -> None:
        """Commit an existing transaction."""

        await self.transaction.__aexit__(*args)

        return None

    @property
    def select_query(self) -> select:
        """Create base select."""
        return select(self.model)

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

    async def create(self, entry_create: BaseSchema, **kwds: Any) -> DBModel:
        """Create a new entry."""

        values = entry_create.dict()
        statement = insert(self.model).values(**(values | kwds))
        entry_id = await self._create_one(statement)

        entry = await self.retrieve_by_id(entry_id)

        return entry

    async def retrieve_by_id(self, id_: UUID) -> DBModel:
        """Get an existing entry by id (primary key)."""

        statement = self.select_query.where(self.model.id == id_)
        entry = await self._retrieve_one(statement)

        return entry

    async def list(self) -> list[DBModel]:
        """Get all existing entries."""

        statement = self.select_query
        entries = await self._retrieve_many(statement)

        return entries

    async def paginate(
        self, pagination: Pagination, sorting: Optional[Sorting] = None, filtering: Optional[Filtering] = None
    ) -> Page:
        """Get all existing entries with pagination support."""

        count_statement = select(func.count()).select_from(self.model)
        if filtering:
            count_statement = filtering.apply(count_statement, self.model)
        count = await self._retrieve_one(count_statement)

        entries_statement = self.select_query.limit(pagination.limit).offset(pagination.offset)
        if sorting:
            entries_statement = sorting.apply(entries_statement, self.model)
        if filtering:
            entries_statement = filtering.apply(entries_statement, self.model)
        entries = await self._retrieve_many(entries_statement)

        return Page(pagination=pagination, count=count, entries=entries)

    async def update(self, id_: UUID, entry_update: BaseSchema, **kwds: Any) -> DBModel:
        """Update an existing entry attributes."""

        values = entry_update.dict(exclude_unset=True, exclude_defaults=True)
        statement = update(self.model).where(self.model.id == id_).values(**(values | kwds))
        await self._update_one(statement)

        entry = await self.retrieve_by_id(id_)

        return entry

    async def delete(self, id_: UUID) -> None:
        """Remove an existing entry."""

        statement = delete(self.model).where(self.model.id == id_)

        await self._delete_one(statement)
