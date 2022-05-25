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

from typing import Type

from pydantic import BaseModel
from sqlalchemy.sql import Select

from project.components import DBModel


class Filtering(BaseModel):
    """Base filtering control parameters."""

    def __bool__(self) -> bool:
        """Filtering considered valid when at least one attribute does not have a default value."""

        values = self.dict()

        for name, field in self.__fields__.items():
            if values[name] != field.default:
                return True

        return False

    def apply(self, statement: Select, model: Type[DBModel]) -> Select:
        """Return statement with applied filtering."""

        raise NotImplementedError
