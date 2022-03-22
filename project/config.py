from functools import lru_cache

from pydantic import BaseSettings
from pydantic import Extra
from pydantic import PostgresDsn


class Settings(BaseSettings):
    """Store service configuration settings."""

    APP_NAME: str = 'project'
    VERSION: str = '0.1.0'
    HOST: str = '127.0.0.1'
    PORT: int = 5064

    RDS_DB_URI: PostgresDsn = 'postgresql://postgres:pilot5kX8@127.0.0.1:6432/postgres'

    OPEN_TELEMETRY_ENABLED: bool = False
    OPEN_TELEMETRY_HOST: str = '127.0.0.1'
    OPEN_TELEMETRY_PORT: int = 6831

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.ignore


@lru_cache(1)
def get_settings() -> Settings:
    settings = Settings()
    return settings
