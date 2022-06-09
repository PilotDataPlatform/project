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
from email.policy import default
from lib2to3.pgen2.token import OP
from typing import Optional

from fastapi import Query
from pydantic import validator

from project.components.parameters import FilterParameters
from project.components.workbench.filtering import WorkbenchFiltering


class WorkbenchFilterParameters(WorkbenchFiltering):
    """Query parameters for workbench filtering."""

    project_id: Optional[str] = Query(default=None)

    def to_filtering(self) -> WorkbenchFiltering:
        return WorkbenchFiltering(
            project_id=self.project_id,
        )
