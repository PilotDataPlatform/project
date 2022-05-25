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

from pydantic import BaseModel

from project.components.models import ModelList


class TestModelList:
    def test_map_by_field_returns_map_based_on_field_argument_as_key(self, fake):
        class Model(BaseModel):
            id: int

        model_1 = Model(id=fake.pyint())
        model_2 = Model(id=fake.pyint())

        models = ModelList([model_1, model_2])

        expected_map = {
            str(model_1.id): model_1,
            str(model_2.id): model_2,
        }

        assert models.map_by_field('id', str) == expected_map
