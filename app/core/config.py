from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    login: str = "/login"


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class JWTConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )
    prefix: ApiPrefix = ApiPrefix()
    run: RunConfig = RunConfig()
    db: DataBaseConfig
    auth: JWTConfig


settings = Settings()
