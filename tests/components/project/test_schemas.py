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

import pytest

from project.components.project.schemas import ProjectSchema


class TestProjectSchema:
    @pytest.mark.parametrize('code', ['0code', 'a', 'aa', 'a' * 33])
    def test_code_field_raises_value_error_for_invalid_values(self, code):
        with pytest.raises(ValueError):
            ProjectSchema(code=code, name='name')

    def test_code_field_strips_whitespaces(self):
        project = ProjectSchema(code=' code ', name='name')

        assert project.code == 'code'

    def test_name_field_strips_whitespaces(self):
        project = ProjectSchema(name=' name ', code='code')

        assert project.name == 'name'
