from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.repositories.role_repository import RoleRepository


@dataclass(frozen=True, slots=True)
class RoleSeed:
    name: str
    description: str
    permissions: dict[str, Any]


PERMISSIONS: tuple[str, ...] = (
    "dashboard:view",
    "alerts:view",
    "alerts:update",
    "alerts:delete",
    "users:create",
    "users:update",
    "users:delete",
    "settings:update",
    "network:view",
    "forensics:view",
    "mitre:view",
)


def _build_permissions(permission_names: tuple[str, ...]) -> dict[str, Any]:
    return {permission_name: True for permission_name in permission_names}


def _read_only_permissions() -> dict[str, Any]:
    return _build_permissions(("dashboard:view", "alerts:view", "network:view", "forensics:view", "mitre:view"))


def _administrator_permissions() -> dict[str, Any]:
    return _build_permissions(PERMISSIONS)


DEFAULT_ROLE_SEEDS: tuple[RoleSeed, ...] = (
    RoleSeed(
        name="Administrator",
        description="Full platform administration with unrestricted access.",
        permissions=_administrator_permissions(),
    ),
    RoleSeed(
        name="SOC Analyst",
        description="Operational monitoring and alert triage for the security operations center.",
        permissions=_build_permissions(("dashboard:view", "alerts:view", "alerts:update", "network:view", "forensics:view", "mitre:view")),
    ),
    RoleSeed(
        name="Incident Responder",
        description="Hands-on incident containment, triage, assignment, and resolution.",
        permissions=_build_permissions(("dashboard:view", "alerts:view", "alerts:update", "alerts:delete", "network:view", "forensics:view", "mitre:view")),
    ),
    RoleSeed(
        name="Threat Hunter",
        description="Proactive threat detection, investigation, and intelligence enrichment.",
        permissions=_build_permissions(("dashboard:view", "alerts:view", "network:view", "forensics:view", "mitre:view")),
    ),
    RoleSeed(
        name="Digital Forensics Analyst",
        description="Evidence preservation, investigation, and reporting for forensic workloads.",
        permissions=_build_permissions(("dashboard:view", "alerts:view", "network:view", "forensics:view", "mitre:view")),
    ),
    RoleSeed(
        name="Viewer",
        description="Read-only access for oversight and reporting use cases.",
        permissions=_read_only_permissions(),
    ),
)


def seed_default_roles(session: Session) -> list[str]:
    role_repository = RoleRepository(session)
    persisted_roles: list[str] = []
    for seed in DEFAULT_ROLE_SEEDS:
        role = role_repository.upsert(
            name=seed.name,
            description=seed.description,
            permissions=seed.permissions,
        )
        persisted_roles.append(role.name)
    session.flush()
    return persisted_roles


def initialize_database(session: Session) -> list[str]:
    return seed_default_roles(session)