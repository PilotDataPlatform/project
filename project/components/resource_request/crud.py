from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.future import select

from project.components.crud import CRUD
from project.components.resource_request.models import ResourceRequest
from project.components.resource_request.schemas import ResourceRequestCreateSchema
from project.components.resource_request.schemas import ResourceRequestUpdateSchema


class ResourceRequestCRUD(CRUD):
    """CRUD for managing resource request database models."""

    model = ResourceRequest

    async def create(self, resource_request_create: ResourceRequestCreateSchema) -> ResourceRequest:
        """Create a new resource request."""

        values = resource_request_create.dict()

        statement = insert(self.model).values(**values)

        resource_request_id = await self.create_one(statement)

        resource_request = await self.retrieve_by_id(resource_request_id)

        return resource_request

    async def retrieve_by_id(self, id_: UUID) -> ResourceRequest:
        """Get an existing resource request by id (primary key)."""

        statement = select(self.model).where(self.model.id == id_)

        resource_request = await self.retrieve_one(statement)

        return resource_request

    async def list(self) -> list[ResourceRequest]:
        """Get all existing resource requests."""

        statement = select(self.model)

        resource_requests = await self.retrieve_many(statement)

        return resource_requests

    async def update(self, id_: UUID, resource_request_update: ResourceRequestUpdateSchema) -> ResourceRequest:
        """Update an existing resource request attributes."""

        values = resource_request_update.dict(exclude_unset=True)

        statement = update(self.model).where(self.model.id == id_).values(**values).returning(self.model)

        await self.update_one(statement)

        resource_request = await self.retrieve_by_id(id_)

        return resource_request

    async def delete(self, id_: UUID) -> None:
        """Remove an existing resource request."""

        statement = delete(self.model).where(self.model.id == id_)

        await self.delete_one(statement)
