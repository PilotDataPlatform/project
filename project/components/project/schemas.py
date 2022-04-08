from typing import Optional
from uuid import UUID

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema


class ProjectSchema(BaseSchema):
    """General project schema."""

    code: str = ''
    name: str = ''
    description: str = ''
    image_url: str = ''
    tags: list[str] = []
    system_tags: list[str] = []
    is_discoverable: bool = False


class ProjectCreateSchema(ProjectSchema):
    """Project schema used for creation."""


class ProjectUpdateSchema(ProjectSchema):
    """Project schema used for update."""

    code: Optional[str]
    name: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    tags: Optional[list[str]]
    system_tags: Optional[list[str]]
    is_discoverable: Optional[bool]


class ProjectResponseSchema(ProjectSchema):
    """Default schema for single project in response."""

    id: UUID

    class Config:
        orm_mode = True


class ProjectListResponseSchema(ListResponseSchema):
    """Default schema for multiple projects in response."""

    result: list[ProjectResponseSchema]
