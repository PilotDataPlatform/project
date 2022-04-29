from datetime import datetime
from uuid import UUID

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema
from project.components.schemas import ParentOptionalFields


class ResourceRequestSchema(BaseSchema):
    """General resource request schema."""

    project_id: UUID
    requested_by_user_id: str = ''
    requested_for: str = ''
    completed_at: datetime = None


class ResourceRequestCreateSchema(ResourceRequestSchema):
    """Resource request schema used for creation."""


class ResourceRequestUpdateSchema(ResourceRequestSchema, metaclass=ParentOptionalFields):
    """Resource request schema used for update."""


class ResourceRequestResponseSchema(ResourceRequestSchema):
    """Default schema for single resource request in response."""

    id: UUID

    class Config:
        orm_mode = True


class ResourceRequestListResponseSchema(ListResponseSchema):
    """Default schema for multiple resource requests in response."""

    result: list[ResourceRequestResponseSchema]
