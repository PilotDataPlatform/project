from typing import Union
from uuid import UUID

from sqlalchemy.future import select

from project.components.crud import CRUD
from project.components.project.models import Project


class ProjectCRUD(CRUD):
    """CRUD for managing project database models."""

    model = Project

    async def retrieve_by_code(self, code: str) -> Project:
        """Get an existing project by unique code."""

        statement = select(self.model).where(self.model.code == code)

        project = await self._retrieve_one(statement)

        return project

    async def retrieve_by_id_or_code(self, id_or_code: Union[UUID, str]) -> Project:
        """Get an existing project either by id or by code (depending on type)."""

        if isinstance(id_or_code, UUID):
            return await self.retrieve_by_id(id_or_code)

        return await self.retrieve_by_code(id_or_code)
