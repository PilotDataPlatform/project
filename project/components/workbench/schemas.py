from datetime import datetime
from uuid import UUID

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema
from project.components.schemas import ParentOptionalFields


class WorkbenchSchema(BaseSchema):
    """General workbench schema."""

    project_id: UUID
    resource: str = ''
    deployed_at: datetime = None
    deployed_by_user_id: str = ''


class WorkbenchCreateSchema(WorkbenchSchema):
    """Workbench schema used for creation."""


class WorkbenchUpdateSchema(WorkbenchSchema, metaclass=ParentOptionalFields):
    """Workbench schema used for update."""


class WorkbenchResponseSchema(WorkbenchSchema):
    """Default schema for single workbench in response."""

    id: UUID

    class Config:
        orm_mode = True


class WorkbenchListResponseSchema(ListResponseSchema):
    """Default schema for multiple workbenches in response."""

    result: list[WorkbenchResponseSchema]
