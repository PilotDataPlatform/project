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

from sqlalchemy.future import select
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import Select

from project.components.crud import CRUD
from project.components.project.models import Project
from project.components.resource_request.models import ResourceRequest


class ResourceRequestCRUD(CRUD):
    """CRUD for managing resource request database models."""

    model = ResourceRequest

    @property
    def select_query(self) -> Select:
        """Return base select including join with Project model."""
        return select(self.model).join(Project).options(contains_eager(self.model.project))
