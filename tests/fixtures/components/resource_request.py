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
from typing import Any
from uuid import UUID

import pytest

from project.components import ResourceRequest
from project.components.models import ModelList
from project.components.resource_request.crud import ResourceRequestCRUD
from project.components.resource_request.schemas import ResourceRequestSchema
from tests.fixtures.components._base_factory import BaseFactory


class ResourceRequestFactory(BaseFactory):
    """Create resource request related entries for testing purposes."""

    def generate(
        self,
        project_id: UUID = ...,
        requested_by_user_id: str = ...,
        requested_for: str = ...,
        completed_at: datetime = ...,
    ) -> ResourceRequestSchema:
        if project_id is ...:
            project_id = self.fake.uuid4(cast_to=None)

        if requested_by_user_id is ...:
            requested_by_user_id = self.fake.uuid4()

        if requested_for is ...:
            requested_for = self.fake.slug()

        if completed_at is ...:
            completed_at = self.fake.past_datetime()

        return ResourceRequestSchema(
            project_id=project_id,
            requested_by_user_id=requested_by_user_id,
            requested_for=requested_for,
            completed_at=completed_at,
        )

    async def create(
        self,
        project_id: UUID = ...,
        requested_by_user_id: str = ...,
        requested_for: str = ...,
        completed_at: datetime = ...,
    ) -> ResourceRequest:
        entry = self.generate(project_id, requested_by_user_id, requested_for, completed_at)

        async with self.crud:
            return await self.crud.create(entry)

    async def bulk_create(
        self,
        number: int,
        project_id: UUID = ...,
        requested_by_user_id: str = ...,
        requested_for: str = ...,
        completed_at: datetime = ...,
        **kwds: Any,
    ) -> ModelList[ResourceRequest]:
        return ModelList(
            [
                await self.create(project_id, requested_by_user_id, requested_for, completed_at, **kwds)
                for _ in range(number)
            ]
        )


@pytest.fixture
def resource_request_crud(db_session) -> ResourceRequestCRUD:
    yield ResourceRequestCRUD(db_session)


@pytest.fixture
def resource_request_factory(resource_request_crud, fake) -> ResourceRequestFactory:
    yield ResourceRequestFactory(resource_request_crud, fake)
