import os
from typing import Annotated, List, Literal

from fastapi import Depends
from pydantic import (
    BaseModel,
    ConfigDict,
)
from pydantic_settings import BaseSettings


class Database(BaseModel):
    """
    Database settings
    """

    user: str
    password: str
    host: str
    database: str
    port: int

    provider: str = "postgresql+psycopg_async"

    @property
    def database_url(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class Settings(BaseSettings):
    """
    FastAPI settings
    """

    model_config = ConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    env: Literal["dev", "prod", "test"] = "dev"
    debug: bool = False
    base_url: str = "http://localhost:8000"
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    timeout: int = 30  # seconds

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    cors_origins: List[str]
    database: Database
    alembic_script_location: str = os.path.join(base_dir, "migrations")
    alembic_ini: str = os.path.join(base_dir, "alembic.ini")
    gpt_key: str


def get_settings():
    return Settings()


settings = get_settings()
SettingsService = Annotated[Settings, Depends(get_settings)]
