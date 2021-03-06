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

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project.components.project.crud import ProjectCRUD
from project.components.project.logo_uploader import LogoUploader
from project.config import Settings
from project.config import get_settings
from project.dependencies import get_db_session
from project.dependencies import get_s3_client
from project.dependencies.s3 import S3Client


def get_project_crud(db_session: AsyncSession = Depends(get_db_session)) -> ProjectCRUD:
    """Return an instance of ProjectCRUD as a dependency."""

    return ProjectCRUD(db_session)


def get_logo_uploader(
    s3_client: S3Client = Depends(get_s3_client), settings: Settings = Depends(get_settings)
) -> LogoUploader:
    """Return an instance of LogoUploader as a dependency."""

    return LogoUploader(s3_client, settings.S3_BUCKET_FOR_PROJECT_LOGOS)
