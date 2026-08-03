from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=False)


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "CyberFusion AI"
    version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    api_prefix: str = "/api"
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@db:5432/cyberfusionai"
    )
    allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
        ]
    )
    jwt_secret_key: str = Field(default="change-me")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7
    jwt_issuer: str = "CyberFusion AI"
    jwt_audience: str = "CyberFusion AI Users"
    auth_password_min_length: int = 12
    auth_password_require_uppercase: bool = True
    auth_password_require_lowercase: bool = True
    auth_password_require_digit: bool = True
    auth_password_require_special: bool = True
    auth_max_failed_login_attempts: int = 5
    auth_lockout_minutes: int = 30
    log_level: str = "INFO"
    log_dir: Path = Field(default_factory=lambda: PROJECT_ROOT / "logs")

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return [str(origin).strip() for origin in value if str(origin).strip()]
        raise TypeError("allowed_origins must be a string or list of strings")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
