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
from typing import Type

from sqlalchemy.sql import Select

from project.components.filtering import Filtering
from project.components.workbench import Workbench


class WorkbenchFiltering(Filtering):
    """Workbenches filtering control parameters."""

    project_id: Optional[str] = None

    def apply(self, statement: Select, model: Type[Workbench]) -> Select:
        """Return statement with applied filtering."""

        if self.project_id:
            statement = statement.where(model.project_id == self.project_id)

        return statement
