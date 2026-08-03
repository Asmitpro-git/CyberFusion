from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, User)

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return self.session.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.session.scalar(statement)

    def get_by_username_or_email(self, identifier: str) -> User | None:
        statement = select(User).where((User.username == identifier) | (User.email == identifier))
        return self.session.scalar(statement)

    def get_with_role_by_id(self, user_id: Any) -> User | None:
        statement = select(User).options(selectinload(User.role)).where(User.id == user_id)
        return self.session.scalar(statement)

    def list_all(self, *, offset: int = 0, limit: int = 100) -> Sequence[User]:
        statement = select(User).order_by(User.username.asc()).offset(offset).limit(limit)
        return self.session.scalars(statement).all()

    def create(
        self,
        *,
        username: str,
        email: str,
        hashed_password: str,
        role_id: Any,
        is_active: bool = True,
        is_verified: bool = False,
        failed_login_attempts: int = 0,
        locked_until: datetime | None = None,
        last_login: datetime | None = None,
    ) -> User:
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role_id=role_id,
            is_active=is_active,
            is_verified=is_verified,
            failed_login_attempts=failed_login_attempts,
            locked_until=locked_until,
            last_login=last_login,
        )
        return super().create(user)

    def update(self, user: User, **changes: Any) -> User:
        for field_name, value in changes.items():
            setattr(user, field_name, value)
        return super().save(user)