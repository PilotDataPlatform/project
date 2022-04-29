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


class Settings(BaseSettings):
    """Store service configuration settings."""

    APP_NAME: str = 'project'
    VERSION: str = '0.1.0'
    HOST: str = '127.0.0.1'
    PORT: int = 5064

    RDS_DB_URI: str = 'postgresql://postgres:pilot5kX8@127.0.0.1:6432/project'
    RDS_ECHO_SQL_QUERIES: bool = False

    OPEN_TELEMETRY_ENABLED: bool = False
    OPEN_TELEMETRY_HOST: str = '127.0.0.1'
    OPEN_TELEMETRY_PORT: int = 6831

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.ignore

    def __init__(self, *args: Any, **kwds: Any) -> None:
        super().__init__(*args, **kwds)

        self.RDS_DB_URI = self.RDS_DB_URI.replace(f'{urlparse(self.RDS_DB_URI).scheme}://', 'postgresql+asyncpg://', 1)


@lru_cache(1)
def get_settings() -> Settings:
    settings = Settings()
    return settings
