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

from os.path import join as urljoin

import pytest

from project.components.project.schemas import ProjectResponseSchema
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


class TestProjectResponseSchema:
    def test_image_url_returns_none_when_logo_name_is_not_set(self, project_factory, fake):
        generated_project = project_factory.generate()
        project = ProjectResponseSchema(
            id=fake.uuid4(), code=generated_project.code, name=generated_project.name, created_at=fake.past_datetime()
        )

        assert project.image_url is None

    def test_image_url_returns_concatenated_url_with_logo_name_and_prefix_from_settings(
        self, project_factory, fake, settings
    ):
        generated_project = project_factory.generate()
        expected_image_url = urljoin(settings.S3_PREFIX_FOR_PROJECT_IMAGE_URLS, generated_project.logo_name)

        project = ProjectResponseSchema(
            id=fake.uuid4(),
            code=generated_project.code,
            name=generated_project.name,
            logo_name=generated_project.logo_name,
            created_at=fake.past_datetime(),
        )

        assert project.image_url == expected_image_url
