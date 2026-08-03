from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Role)

    def get_by_name(self, name: str) -> Role | None:
        statement = select(Role).where(Role.name == name)
        return self.session.scalar(statement)

    def list_all(self, *, offset: int = 0, limit: int = 100) -> Sequence[Role]:
        statement = select(Role).order_by(Role.name.asc()).offset(offset).limit(limit)
        return self.session.scalars(statement).all()

    def create(self, *, name: str, description: str | None, permissions: dict[str, Any]) -> Role:
        role = Role(name=name, description=description, permissions=permissions)
        return super().create(role)

    def update(
        self,
        role: Role,
        *,
        name: str | None = None,
        description: str | None = None,
        permissions: dict[str, Any] | None = None,
    ) -> Role:
        if name is not None:
            role.name = name
        if description is not None:
            role.description = description
        if permissions is not None:
            role.permissions = permissions
        return super().save(role)

    def upsert(
        self,
        *,
        name: str,
        description: str | None,
        permissions: dict[str, Any],
    ) -> Role:
        role = self.get_by_name(name)
        if role is None:
            return self.create(name=name, description=description, permissions=permissions)
        return self.update(role, description=description, permissions=permissions)