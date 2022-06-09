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

from uuid import UUID

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema
from project.components.schemas import ParentOptionalFields


class WorkbenchSchema(BaseSchema):
    """General workbench schema."""

    project_id: UUID
    resource: str = ''
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
