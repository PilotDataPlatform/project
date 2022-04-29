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

from typing import Optional
from uuid import UUID

from pydantic import HttpUrl
from pydantic import constr

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema
from project.components.schemas import ParentOptionalFields


class ProjectSchema(BaseSchema):
    """General project schema."""

    code: constr(min_length=3, max_length=32, regex=r'^[a-z][a-z0-9]*$', strip_whitespace=True)  # noqa: F722
    name: constr(min_length=3, max_length=256, strip_whitespace=True)
    description: constr(max_length=256, strip_whitespace=True) = ''
    image_url: Optional[HttpUrl] = None
    tags: list[constr(max_length=256, strip_whitespace=True)] = []
    system_tags: list[constr(max_length=256)] = []
    is_discoverable: bool = False


class ProjectCreateSchema(ProjectSchema):
    """Project schema used for creation."""


class ProjectUpdateSchema(ProjectSchema, metaclass=ParentOptionalFields):
    """Project schema used for update."""


class ProjectResponseSchema(ProjectSchema):
    """Default schema for single project in response."""

    id: UUID

    class Config:
        orm_mode = True


class ProjectListResponseSchema(ListResponseSchema):
    """Default schema for multiple projects in response."""

    result: list[ProjectResponseSchema]
