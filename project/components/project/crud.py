from typing import Union
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.future import select

from project.components.crud import CRUD
from project.components.project.models import Project
from project.components.project.schemas import ProjectCreateSchema
from project.components.project.schemas import ProjectUpdateSchema


class ProjectCRUD(CRUD):
    """CRUD for managing project database models."""

    model = Project

    async def create(self, project_create: ProjectCreateSchema) -> Project:
        """Create a new project."""

        values = project_create.dict()

        statement = insert(self.model).values(**values)

        project_id = await self.create_one(statement)

        project = await self.retrieve_by_id(project_id)

        return project

    async def retrieve_by_id(self, id_: UUID) -> Project:
        """Get an existing project by id (primary key)."""

        statement = select(self.model).where(self.model.id == id_)

        project = await self.retrieve_one(statement)

        return project

    async def retrieve_by_code(self, code: str) -> Project:
        """Get an existing project by unique code."""

        statement = select(self.model).where(self.model.code == code)

        project = await self.retrieve_one(statement)

        return project

    async def retrieve_by_id_or_code(self, id_or_code: Union[UUID, str]) -> Project:
        """Get an existing project either by id or by code (depending on type)."""

        if isinstance(id_or_code, UUID):
            return await self.retrieve_by_id(id_or_code)

        return await self.retrieve_by_code(id_or_code)

    async def list(self) -> list[Project]:
        """Get all existing projects."""

        statement = select(self.model)

        projects = await self.retrieve_many(statement)

        return projects

    async def update(self, id_: UUID, project_update: ProjectUpdateSchema) -> Project:
        """Update an existing project attributes."""

        values = project_update.dict(exclude_unset=True)

        statement = update(self.model).where(self.model.id == id_).values(**values).returning(self.model)

        await self.update_one(statement)

        project = await self.retrieve_by_id(id_)

        return project

    async def delete(self, id_: UUID) -> None:
        """Remove an existing project."""

        statement = delete(self.model).where(self.model.id == id_)

        await self.delete_one(statement)
