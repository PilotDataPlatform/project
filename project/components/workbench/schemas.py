from datetime import datetime
from typing import Optional
from uuid import UUID

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema


class WorkbenchSchema(BaseSchema):
    """General workbench schema."""

    project_id: UUID
    resource: str = ''
    deployed_at: datetime = None
    deployed_by_user_id: str = ''


class WorkbenchCreateSchema(WorkbenchSchema):
    """Workbench schema used for creation."""


class WorkbenchUpdateSchema(WorkbenchSchema):
    """Workbench schema used for update."""

    project_id: Optional[UUID]
    resource: Optional[str]
    deployed_at: Optional[datetime]
    deployed_by_user_id: Optional[str]


class WorkbenchResponseSchema(WorkbenchSchema):
    """Default schema for single workbench in response."""

    id: UUID

    class Config:
        orm_mode = True


class WorkbenchListResponseSchema(ListResponseSchema):
    """Default schema for multiple workbenches in response."""

    result: list[WorkbenchResponseSchema]
