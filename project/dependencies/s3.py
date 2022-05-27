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

from typing import NewType

from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session
from botocore.config import Config
from fastapi import Depends

from project.config import Settings
from project.config import get_settings

S3Client = NewType('S3Client', AioBaseClient)


async def get_s3_client(settings: Settings = Depends(get_settings)) -> S3Client:
    """Create a FastAPI callable dependency for Boto3 Client instance."""

    session = get_session()
    async with session.create_client(
        's3',
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        endpoint_url=settings.S3_ENDPOINT_URL,
        config=Config(signature_version='s3v4'),
    ) as client:
        return client
