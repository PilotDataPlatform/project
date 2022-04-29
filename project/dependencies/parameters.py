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

from fastapi import Query
from pydantic import BaseModel

from project.components.pagination import Pagination


class PageParameters(BaseModel):
    """Query parameters for pagination."""

    page: int = Query(default=0, ge=0)
    page_size: int = Query(default=20, ge=1)

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, page_size=self.page_size)
