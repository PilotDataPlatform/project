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

from __future__ import annotations

from typing import Optional
from typing import Type

from fastapi import Query
from pydantic import BaseModel
from pydantic import create_model

from project.components.filtering import Filtering
from project.components.pagination import Pagination
from project.components.sorting import Sorting
from project.components.sorting import SortingOrder
from project.components.types import StrEnum


class QueryParameters(BaseModel):
    """Base class for class-based query parameters definition."""


class PageParameters(QueryParameters):
    """Base query parameters for pagination."""

    page: int = Query(default=0, ge=0)
    page_size: int = Query(default=20, ge=1)

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, page_size=self.page_size)


class SortByFields(StrEnum):
    """Base class for defining sort by fields."""


class SortParameters(QueryParameters):
    """Base query parameters for sorting."""

    sort_by: Optional[str] = Query(default=None)
    sort_order: Optional[SortingOrder] = Query(default=SortingOrder.ASC)

    @classmethod
    def with_sort_by_fields(cls, fields: Type[SortByFields]) -> Type[SortParameters]:
        """Limit sort_by field with values specified in fields argument."""

        return create_model(cls.__name__, __base__=cls, sort_by=(Optional[fields], Query(default=None)))

    def to_sorting(self) -> Sorting:
        field = self.sort_by

        if isinstance(field, SortByFields):
            field = field.value

        return Sorting(field=field, order=self.sort_order)


class FilterParameters(QueryParameters):
    """Base query parameters for filtering."""

    def to_filtering(self) -> Filtering:
        raise NotImplementedError
