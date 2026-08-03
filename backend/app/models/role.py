from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class Role(BaseModel):
    """
    Enterprise Role model.
    """

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    permissions: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    users: Mapped[list["User"]] = relationship(
        back_populates="role",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Role(name='{self.name}')>"