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
from typing import Optional
from typing import Type

from sqlalchemy.sql import Select

from project.components.filtering import Filtering
from project.components.project import Project


class ProjectFiltering(Filtering):
    """Projects filtering control parameters."""

    name: Optional[str] = None
    code: Optional[str] = None
    codes: Optional[list[str]] = None
    description: Optional[str] = None
    created_at: Optional[tuple[datetime, datetime]] = None
    tags: Optional[list[str]] = None
    is_discoverable: Optional[bool] = None

    def apply(self, statement: Select, model: Type[Project]) -> Select:
        """Return statement with applied filtering."""

        if self.name:
            statement = statement.where(model.name.ilike(self.name))

        if self.code:
            statement = statement.where(model.code.ilike(self.code))

        if self.codes:
            statement = statement.where(model.code.in_(self.codes))

        if self.description:
            statement = statement.where(model.description.ilike(self.description))

        if self.created_at:
            statement = statement.where(model.created_at.between(*self.created_at))

        if self.tags:
            statement = statement.where(model.tags.contains(self.tags))

        if self.is_discoverable is not None:
            statement = statement.where(model.is_discoverable == self.is_discoverable)

        return statement
