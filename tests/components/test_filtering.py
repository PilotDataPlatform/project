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

from project.components.filtering import Filtering


class TestFiltering:
    def test__bool__returns_true_when_at_least_one_attribute_is_set(self):
        class CustomFiltering(Filtering):
            field: Optional[list[str]] = None

        filtering = CustomFiltering(field=['value'])

        assert bool(filtering) is True

    def test__bool__returns_false_when_all_attributes_are_not_set(self):
        class CustomFiltering(Filtering):
            field: Optional[int] = None

        filtering = CustomFiltering()

        assert bool(filtering) is False
