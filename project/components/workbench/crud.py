from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.future import select

from project.components.crud import CRUD
from project.components.workbench.models import Workbench
from project.components.workbench.schemas import WorkbenchCreateSchema
from project.components.workbench.schemas import WorkbenchUpdateSchema


class WorkbenchCRUD(CRUD):
    """CRUD for managing workbench database models."""

    model = Workbench

    async def create(self, workbench_create: WorkbenchCreateSchema) -> Workbench:
        """Create a new workbench."""

        values = workbench_create.dict()

        statement = insert(self.model).values(**values)

        workbench_id = await self.create_one(statement)

        workbench = await self.retrieve_by_id(workbench_id)

        return workbench

    async def retrieve_by_id(self, id_: UUID) -> Workbench:
        """Get an existing workbench by id (primary key)."""

        statement = select(self.model).where(self.model.id == id_)

        workbench = await self.retrieve_one(statement)

        return workbench

    async def list(self) -> list[Workbench]:
        """Get all existing workbenches."""

        statement = select(self.model)

        workbenches = await self.retrieve_many(statement)

        return workbenches

    async def update(self, id_: UUID, workbench_update: WorkbenchUpdateSchema) -> Workbench:
        """Update an existing workbench attributes."""

        values = workbench_update.dict(exclude_unset=True)

        statement = update(self.model).where(self.model.id == id_).values(**values).returning(self.model)

        await self.update_one(statement)

        workbench = await self.retrieve_by_id(id_)

        return workbench

    async def delete(self, id_: UUID) -> None:
        """Remove an existing workbench."""

        statement = delete(self.model).where(self.model.id == id_)

        await self.delete_one(statement)
