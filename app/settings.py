import os
from typing import Annotated, List, Literal

from fastapi import Depends
from pydantic import (
    BaseModel,
    Field,
)
from pydantic_settings import BaseSettings


class Database(BaseModel):
    """
    Database settings
    """

    user: str       = Field(...,            env="USER")
    password: str   = Field(...,            env="PASSWORD")
    host: str       = Field(default="localhost", env="HOST")
    database: str   = Field(...,            env="DATABASE")
    port: int       = Field(default=5432,   env="PORT")

    provider: str   = "postgresql+psycopg_async"

    @property
    def database_url(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class Settings(BaseSettings):
    """
    FastAPI settings
    """

    env: Literal["dev", "prod", "test"] = "dev"
    debug: bool = False
    base_url: str = "http://localhost:8000"
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    timeout: int = 30  # seconds

    # secret_key: str
    cors_origins: List[str]
    database: Database
    gpt_key: str

    class Config:
        env_file = (os.path.join(os.path.dirname(__file__), ".env"),)
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        case_sensitive = False
        extra = "ignore"


def get_settings():
    return Settings()


settings = get_settings()
SettingsService = Annotated[Settings, Depends(get_settings)]
