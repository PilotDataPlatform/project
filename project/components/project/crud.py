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

from typing import Union
from uuid import UUID

from sqlalchemy.future import select

from project.components.crud import CRUD
from project.components.project.models import Project


class ProjectCRUD(CRUD):
    """CRUD for managing project database models."""

    model = Project

    async def retrieve_by_code(self, code: str) -> Project:
        """Get an existing project by unique code."""

        statement = select(self.model).where(self.model.code == code)

        project = await self._retrieve_one(statement)

        return project

    async def retrieve_by_id_or_code(self, id_or_code: Union[UUID, str]) -> Project:
        """Get an existing project either by id or by code (depending on type)."""

        if isinstance(id_or_code, UUID):
            return await self.retrieve_by_id(id_or_code)

        return await self.retrieve_by_code(id_or_code)
