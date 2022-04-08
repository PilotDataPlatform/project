from datetime import datetime
from typing import Optional
from uuid import UUID

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema


class ResourceRequestSchema(BaseSchema):
    """General resource request schema."""

    project_id: UUID
    requested_by_user_id: str = ''
    requested_for: str = ''
    completed_at: datetime = None


class ResourceRequestCreateSchema(ResourceRequestSchema):
    """Resource request schema used for creation."""


class ResourceRequestUpdateSchema(ResourceRequestSchema):
    """Resource request schema used for update."""

    project_id: Optional[UUID]
    requested_by_user_id: Optional[str]
    requested_for: Optional[str]
    completed_at: Optional[datetime]


class ResourceRequestResponseSchema(ResourceRequestSchema):
    """Default schema for single resource request in response."""

    id: UUID

    class Config:
        orm_mode = True


class ResourceRequestListResponseSchema(ListResponseSchema):
    """Default schema for multiple resource requests in response."""

    result: list[ResourceRequestResponseSchema]
