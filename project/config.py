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

from functools import lru_cache
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseSettings
from pydantic import Extra
from pydantic import Field
from pydantic import HttpUrl
from pydantic import validator
from pydantic.fields import ModelField


class Settings(BaseSettings):
    """Store service configuration settings."""

    APP_NAME: str = 'project'
    VERSION: str = '0.1.0'
    HOST: str = '127.0.0.1'
    PORT: int = 5064
    WORKERS: int = 1

    RDS_DB_HOST: str = Field('127.0.0.1', env={'RDS_DB_HOST', 'OPSDB_UTILITY_HOST'})
    RDS_DB_PORT: int = Field(6432, env={'RDS_DB_PORT', 'OPSDB_UTILITY_PORT'})
    RDS_DB_USERNAME: str = Field('postgres', env={'RDS_DB_USERNAME', 'OPSDB_UTILITY_USERNAME'})
    RDS_DB_PASSWORD: str = Field('pilot5kX8', env={'RDS_DB_PASSWORD', 'OPSDB_UTILITY_PASSWORD'})
    RDS_DB_NAME: str = 'project'
    RDS_DB_URI: str = 'postgresql://postgres:pilot5kX8@127.0.0.1:6432/project'
    RDS_ECHO_SQL_QUERIES: bool = False

    S3_ENDPOINT_URL: HttpUrl = 'http://127.0.0.1:9100'
    S3_ACCESS_KEY: str = 'GMIMPKTWGOKHIQYYQHPO'
    S3_SECRET_KEY: str = 'KLdvMcrHMVnar/HJGKVAS/TRglfFvzDrbYpdknbc'
    S3_BUCKET_FOR_PROJECT_LOGOS: str = 'project-logos'
    S3_PREFIX_FOR_PROJECT_IMAGE_URLS: HttpUrl = 'http://127.0.0.1:9100/project-logos'

    OPEN_TELEMETRY_ENABLED: bool = False
    OPEN_TELEMETRY_HOST: str = '127.0.0.1'
    OPEN_TELEMETRY_PORT: int = 6831

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.ignore

    @validator('RDS_DB_URI')
    def uri_must_have_value(cls, value: str, values: dict[str, Any], field: ModelField) -> str:
        """Make sure that `RDS_DB_URI` always has an appropriate value.

        Value set for `RDS_DB_URI` always has a priority over concatenated `RDS_DB_*` values.
        """

        if value != field.default:
            return value

        db_uri = (
            f'postgresql://{values["RDS_DB_USERNAME"]}:{values["RDS_DB_PASSWORD"]}'
            f'@{values["RDS_DB_HOST"]}:{values["RDS_DB_PORT"]}/{values["RDS_DB_NAME"]}'
        )
        if db_uri != value:
            return db_uri

        return value

    def __init__(self, *args: Any, **kwds: Any) -> None:
        super().__init__(*args, **kwds)

        self.RDS_DB_URI = self.RDS_DB_URI.replace(f'{urlparse(self.RDS_DB_URI).scheme}://', 'postgresql+asyncpg://', 1)


@lru_cache(1)
def get_settings() -> Settings:
    settings = Settings()
    return settings
