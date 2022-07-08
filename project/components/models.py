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

    def map_by_field(self, field: str, key_type: Optional[type] = None) -> dict[Any, Any]:
        """Create map using field argument as key with optional type casting."""

        results = {}
        for source in self:
            try:
                key = getattr(source, field)
            except AttributeError:
                relationship, relationship_field = field.split('.')
                key = getattr(source, relationship)
                key = getattr(key, relationship_field)

            if key_type is not None:
                key = key_type(key)

            results[key] = source

        return results
