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

from project.components.types import StrEnum


class TestStrEnum:
    def test_values_returns_list_of_enum_values(self):
        class CustomStrEnum(StrEnum):
            KEY1 = 'value1'
            KEY2 = 'value2'

        expected_values = ['value1', 'value2']

        assert CustomStrEnum.values() == expected_values
