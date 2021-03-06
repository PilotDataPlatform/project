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

from sqlalchemy.sql import Select

from project.components.project.models import Project
from project.components.resource_request.models import ResourceRequest
from project.components.sorting import Sorting


class ResourceRequestSorting(Sorting):
    """Resource request sorting control parameters."""

    def apply(self, statement: Select, model: ResourceRequest) -> Select:
        """Return statement with applied ordering.

        This is necessary to allow sorting by fields from the relationship model.
        """
        try:
            _, relationship_field = self.field.split('.', 1)
            self.field = relationship_field
            model = Project
        except ValueError:
            pass
        return super().apply(statement, model)
