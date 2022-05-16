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

from base64 import b64encode
from io import BytesIO

import faker
import pytest
from PIL import Image


class Faker(faker.Faker):
    def image(self, size: tuple[int, int] = (512, 512), format_type: str = 'PNG') -> bytes:
        """Generate an image."""

        buffer = BytesIO()
        color = self.color(hue='red')
        image = Image.new('RGB', size, color)
        image.save(buffer, format_type)

        return buffer.getvalue()

    def base64_image(self, size: tuple[int, int] = (512, 512), format_type: str = 'PNG') -> str:
        """Generate an image as base64 string."""

        image = self.image(size, format_type)

        return b64encode(image).decode()


@pytest.fixture
def fake() -> Faker:
    yield Faker()
