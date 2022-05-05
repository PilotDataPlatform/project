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
from unittest.mock import AsyncMock

import pytest

from project.dependencies.s3 import S3Client


class MockS3Client:
    def __init__(self) -> None:
        self.mock = AsyncMock()

    async def __aenter__(self) -> S3Client:
        return self.mock

    async def __aexit__(self, *args: Any) -> None:
        return None

    def __getattr__(self, name: str) -> Any:
        return getattr(self.mock, name)


@pytest.fixture
def s3_client() -> S3Client:
    yield MockS3Client()
