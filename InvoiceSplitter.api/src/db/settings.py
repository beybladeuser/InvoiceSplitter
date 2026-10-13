from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_REPOSITORY_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: SecretStr

    @property
    def url(self) -> URL:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.database_user,
            password=self.database_password.get_secret_value(),
            host=self.database_host,
            port=self.database_port,
            database=self.database_name,
        )
