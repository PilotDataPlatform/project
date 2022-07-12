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

from typing import Any
from typing import Optional


class ModelList(list):
    """Store a list of models of the same type."""

    def _get_nested_field(self, source, key):
        try:
            relationship, relationship_field = key.split('.', 1)
            source = getattr(source, relationship)
            return self._get_nested_field(source, relationship_field)
        except ValueError:
            return getattr(source, key)

    def map_by_field(self, field: str, key_type: Optional[type] = None) -> dict[Any, Any]:
        """Create map using field argument as key with optional type casting."""

        results = {}
        for source in self:
            key = self._get_nested_field(source, field)
            results[key] = source

        return results

    def get_field_values(self, field: str) -> list[Any]:
        """Return list with values each model has in field attribute."""
        field_values_list = []
        for source in self:
            field_values_list.append(self._get_nested_field(source, field))
        return field_values_list
