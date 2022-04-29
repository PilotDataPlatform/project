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

from datetime import datetime
from uuid import UUID

import pytest

from project.components import Workbench
from project.components.workbench.crud import WorkbenchCRUD
from project.components.workbench.schemas import WorkbenchSchema
from tests.fixtures.components._base_factory import BaseFactory


class WorkbenchFactory(BaseFactory):
    """Create workbench related entries for testing purposes."""

    def generate(
        self,
        project_id: UUID = ...,
        resource: str = ...,
        deployed_at: datetime = ...,
        deployed_by_user_id: str = ...,
    ) -> WorkbenchSchema:
        if project_id is ...:
            project_id = self.fake.uuid4(cast_to=None)

        if resource is ...:
            resource = self.fake.word()

        if deployed_at is ...:
            deployed_at = self.fake.past_datetime()

        if deployed_by_user_id is ...:
            deployed_by_user_id = self.fake.uuid4()

        return WorkbenchSchema(
            project_id=project_id,
            resource=resource,
            deployed_at=deployed_at,
            deployed_by_user_id=deployed_by_user_id,
        )

    async def create(
        self,
        project_id: UUID = ...,
        resource: str = ...,
        deployed_at: datetime = ...,
        deployed_by_user_id: str = ...,
    ) -> Workbench:
        entry = self.generate(project_id, resource, deployed_at, deployed_by_user_id)

        async with self.crud:
            return await self.crud.create(entry)


@pytest.fixture
def workbench_crud(db_session) -> WorkbenchCRUD:
    yield WorkbenchCRUD(db_session)


@pytest.fixture
def workbench_factory(workbench_crud, fake) -> WorkbenchFactory:
    yield WorkbenchFactory(workbench_crud, fake)
