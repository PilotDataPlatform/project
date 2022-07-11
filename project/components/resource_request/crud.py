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

from sqlalchemy import func
from sqlalchemy.future import select

from project.components.crud import CRUD
from project.components.filtering import Filtering
from project.components.pagination import Page
from project.components.pagination import Pagination
from project.components.project.models import Project
from project.components.resource_request.models import ResourceRequest
from project.components.sorting import Sorting


class ResourceRequestCRUD(CRUD):
    """CRUD for managing resource request database models."""

    model = ResourceRequest

    async def paginate(
        self, pagination: Pagination, sorting: Optional[Sorting] = None, filtering: Optional[Filtering] = None
    ) -> Page:
        """Get all existing entries with pagination support."""

        count_statement = select(func.count()).select_from(self.model)
        if filtering:
            count_statement = filtering.apply(count_statement, self.model)
        count = await self._retrieve_one(count_statement)

        entries_statement = select(self.model).join(Project).limit(pagination.limit).offset(pagination.offset)
        if sorting:
            try:
                _, relationship_field = sorting.field.split('.')
                sorting.field = relationship_field
                entries_statement = sorting.apply(entries_statement, Project)
            except ValueError:
                entries_statement = sorting.apply(entries_statement, self.model)
        if filtering:
            entries_statement = filtering.apply(entries_statement, self.model)
        entries = await self._retrieve_many(entries_statement)

        return Page(pagination=pagination, count=count, entries=entries)
