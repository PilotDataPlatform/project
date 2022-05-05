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

import asyncio
import logging
from functools import partial
from io import BytesIO

from PIL import Image

from project.dependencies.s3 import S3Client

logger = logging.getLogger(__name__)


class BucketNotFound(Exception):
    """Raised when specified bucket is not found."""


class LogoUploader:
    """Perform image conversion and upload to S3 bucket."""

    def __init__(self, s3_client: S3Client, s3_bucket_name: str) -> None:
        self.s3_client = s3_client
        self.s3_bucket_name = s3_bucket_name

    def convert_sync(self, image: bytes, resize_size: tuple[int, int] = (200, 200), output_type: str = 'PNG') -> bytes:
        """Convert and resize image synchronously."""

        buffer = BytesIO()

        try:
            img = Image.open(BytesIO(image))
            img = img.resize(resize_size, Image.Resampling.LANCZOS)
            img.save(buffer, output_type)
        except Exception:
            logger.exception('Unable to convert image.')
            raise

        return buffer.getvalue()

    async def convert(self, image: bytes) -> bytes:
        """Convert and resize image."""

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(self.convert_sync, image))

    async def create_bucket(self) -> None:
        """Create new S3 bucket."""

        async with self.s3_client as client:
            try:
                logger.info(f'Trying to create bucket "{self.s3_bucket_name}".')
                await client.create_bucket(Bucket=self.s3_bucket_name)
            except Exception:
                logger.exception(f'Unable to create bucket "{self.s3_bucket_name}".')
                raise

    async def upload(self, image: bytes, filename: str) -> None:
        """Upload image to S3 bucket."""

        async with self.s3_client as client:
            try:
                logger.info(f'Trying to upload file "{filename}" into the "{self.s3_bucket_name}" bucket')
                await client.put_object(Bucket=self.s3_bucket_name, Key=filename, Body=image)
                logger.info(f'File "{filename}" has been uploaded to the "{self.s3_bucket_name}" bucket.')
            except client.exceptions.NoSuchBucket:
                logger.exception(f'Bucket "{self.s3_bucket_name}" does not exist.')
                raise BucketNotFound
            except Exception:
                logger.exception(f'Unable to upload file "{filename}" into the "{self.s3_bucket_name}" bucket.')
                raise

    async def convert_and_upload(self, image: bytes, filename: str) -> None:
        """Convert image and upload to S3 bucket.

        Create bucket if it does not exist.
        """

        converted_image = await self.convert(image)

        try:
            await self.upload(converted_image, filename)
        except BucketNotFound:
            await self.create_bucket()
            await self.upload(converted_image, filename)
