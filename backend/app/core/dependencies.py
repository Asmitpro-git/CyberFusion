from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.settings import Settings, get_settings
from app.database.session import get_db


def get_app_settings() -> Settings:
    return get_settings()


def get_database_session() -> Generator[Session, None, None]:
    yield from get_db()


AppSettings = Depends(get_app_settings)
DatabaseSession = Depends(get_database_session)