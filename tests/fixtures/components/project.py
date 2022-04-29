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

from project.components import Project
from project.components.project.crud import ProjectCRUD
from project.components.project.schemas import ProjectSchema
from tests.fixtures.components._base_factory import BaseFactory


class ProjectFactory(BaseFactory):
    """Create project related entries for testing purposes."""

    def generate(
        self,
        code: str = ...,
        name: str = ...,
        description: str = ...,
        image_url: str = ...,
        tags: list[str] = ...,
        system_tags: list[str] = ...,
        is_discoverable: bool = ...,
    ) -> ProjectSchema:
        if code is ...:
            code = self.fake.pystr_format('?#' * 10).lower()

        if name is ...:
            name = code

        if description is ...:
            description = self.fake.sentence()

        if image_url is ...:
            image_url = self.fake.image_url()

        if tags is ...:
            tags = self.fake.words(3, unique=True)

        if system_tags is ...:
            system_tags = self.fake.words(2, unique=True)

        if is_discoverable is ...:
            is_discoverable = True

        return ProjectSchema(
            code=code,
            name=name,
            description=description,
            image_url=image_url,
            tags=tags,
            system_tags=system_tags,
            is_discoverable=is_discoverable,
        )

    async def create(
        self,
        code: str = ...,
        name: str = ...,
        description: str = ...,
        image_url: str = ...,
        tags: list[str] = ...,
        system_tags: list[str] = ...,
        is_discoverable: bool = ...,
    ) -> Project:
        entry = self.generate(code, name, description, image_url, tags, system_tags, is_discoverable)

        async with self.crud:
            return await self.crud.create(entry)


@pytest.fixture
def project_crud(db_session) -> ProjectCRUD:
    yield ProjectCRUD(db_session)


@pytest.fixture
def project_factory(project_crud, fake) -> ProjectFactory:
    yield ProjectFactory(project_crud, fake)
