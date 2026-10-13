from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_REPOSITORY_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "invoicesplitter"
    database_user: str = "invoicesplitter"
    database_password: SecretStr = Field(
        validation_alias=AliasChoices("DATABASE_PASSWORD", "POSTGRES_PASSWORD")
    )

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
