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
from typing import Type

import jq as json_processor
import pytest
from httpx import Response


class JQResult:
    """Typing for jq processor response."""

    def all(self) -> list[Any]:
        ...

    def first(self) -> Any:
        ...

    def text(self) -> str:
        ...


class JQ:
    """Perform jq queries against httpx json response."""

    def __init__(self, response: Response) -> None:
        self.json = response.json()

    def __call__(self, query: str) -> JQResult:
        return json_processor.compile(query).input(self.json)


@pytest.fixture
def jq() -> Type[JQ]:
    yield JQ
