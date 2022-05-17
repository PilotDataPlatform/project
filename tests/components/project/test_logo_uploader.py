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

import magic
import pytest

from project.components.project.logo_uploader import LogoUploader


@pytest.fixture
def logo_uploader(s3_client) -> LogoUploader:
    yield LogoUploader(s3_client, 's3_bucket_name')


class TestLogoUploader:
    def test_convert_sync_returns_converted_png_image(self, logo_uploader, fake):
        image = fake.image()

        converted_image = logo_uploader.convert_sync(image)
        received_mime_type = magic.from_buffer(converted_image, mime=True)

        assert received_mime_type == 'image/png'

    async def test_convert_returns_converted_png_image(self, logo_uploader, fake):
        image = fake.image()

        converted_image = await logo_uploader.convert(image)
        received_mime_type = magic.from_buffer(converted_image, mime=True)

        assert received_mime_type == 'image/png'

    async def test_create_bucket_calls_create_bucket_method(self, logo_uploader, fake):
        logo_uploader.s3_bucket_name = fake.pystr(20)

        await logo_uploader.create_bucket()

        logo_uploader.s3_client.create_bucket.assert_called_once()

    async def test_convert_and_upload_calls_upload_second_time_after_bucket_creation(self, logo_uploader, fake):
        image = fake.image()
        filename = fake.file_name(extension='png')

        logo_uploader.s3_bucket_name = fake.pystr(20)

        exception = Exception
        logo_uploader.s3_client.exceptions.NoSuchBucket = exception
        logo_uploader.s3_client.put_object.side_effect = [exception(), None]

        await logo_uploader.convert_and_upload(image, filename)

        assert logo_uploader.s3_client.put_object.call_count == 2
