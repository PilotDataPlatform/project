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

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema
from project.components.schemas import ParentOptionalFields


class ResourceRequestSchema(BaseSchema):
    """General resource request schema."""

    project_id: UUID
    user_id: str
    email: EmailStr
    username: str
    requested_for: str
    completed_at: datetime = None


class ResourceRequestCreateSchema(ResourceRequestSchema):
    """Resource request schema used for creation."""


class ResourceRequestUpdateSchema(ResourceRequestSchema, metaclass=ParentOptionalFields):
    """Resource request schema used for update."""


class ResourceRequestResponseSchema(ResourceRequestSchema):
    """Default schema for single resource request in response."""

    id: UUID
    requested_at: datetime

    class Config:
        orm_mode = True


class ResourceRequestListResponseSchema(ListResponseSchema):
    """Default schema for multiple resource requests in response."""

    result: list[ResourceRequestResponseSchema]
