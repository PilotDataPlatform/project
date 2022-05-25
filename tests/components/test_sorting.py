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

from project.components.sorting import Sorting
from project.components.sorting import SortingOrder


class TestSorting:
    def test__bool__returns_true_when_field_attribute_is_set(self):
        sorting = Sorting(field='value', order=SortingOrder.ASC)

        assert bool(sorting) is True

    def test__bool__returns_false_when_field_attribute_is_not_set(self):
        sorting = Sorting(order=SortingOrder.DESC)

        assert bool(sorting) is False
