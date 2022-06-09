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

from fastapi import Query

from project.components.workbench.filtering import WorkbenchesFiltering


class WorkbenchFilterParameters(WorkbenchesFiltering):
    """Query parameters for workbench filtering."""

    project_id: Optional[str] = Query(default=None)

    def to_filtering(self) -> WorkbenchesFiltering:
        return WorkbenchesFiltering(
            project_id=self.project_id,
        )
