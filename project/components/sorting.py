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

from pydantic import BaseModel
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy.sql import Select

from project.components import DBModel
from project.components.types import StrEnum


class SortingOrder(StrEnum):
    """Available sorting orders."""

    ASC = 'asc'
    DESC = 'desc'


class Sorting(BaseModel):
    """Base sorting control parameters."""

    field: Optional[str] = None
    order: SortingOrder

    def __bool__(self) -> bool:
        """Sorting considered valid when the field is specified."""

        return self.field is not None

    def apply(self, statement: Select, model: Type[DBModel]) -> Select:
        """Return statement with applied ordering."""

        field = getattr(model, self.field)

        order_by = asc(field)
        if self.order is SortingOrder.DESC:
            order_by = desc(field)

        return statement.order_by(order_by)
