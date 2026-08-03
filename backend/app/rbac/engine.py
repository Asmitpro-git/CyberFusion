from __future__ import annotations

from collections.abc import Iterable
from typing import Any


class PermissionEngine:
    PERMISSIONS = {
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
    }

    @classmethod
    def normalize(cls, permissions: Any) -> set[str]:
        normalized: set[str] = set()
        if permissions is None:
            return normalized
        if isinstance(permissions, str):
            token = permissions.strip()
            if token:
                normalized.add(token)
            return normalized
        if isinstance(permissions, dict):
            for key, value in permissions.items():
                if isinstance(value, bool):
                    if value:
                        normalized.add(str(key).strip())
                else:
                    normalized.update(cls.normalize(value))
            return normalized
        if isinstance(permissions, Iterable):
            for item in permissions:
                normalized.update(cls.normalize(item))
            return normalized
        token = str(permissions).strip()
        if token:
            normalized.add(token)
        return normalized

    @classmethod
    def has_permission(cls, granted_permissions: Any, required_permission: str) -> bool:
        if required_permission not in cls.PERMISSIONS:
            return False
        normalized = cls.normalize(granted_permissions)
        if "*" in normalized or "all" in normalized:
            return True
        return required_permission in normalized

    @classmethod
    def has_permissions(cls, granted_permissions: Any, required_permissions: Iterable[str]) -> bool:
        return all(cls.has_permission(granted_permissions, permission) for permission in required_permissions)


class RoleEngine:
    ADMINISTRATOR_ROLE = "Administrator"

    @classmethod
    def normalize(cls, role_name: Any) -> str:
        return str(role_name or "").strip()

    @classmethod
    def has_role(cls, current_role: Any, required_role: str) -> bool:
        normalized_current = cls.normalize(current_role)
        normalized_required = cls.normalize(required_role)
        if not normalized_current or not normalized_required:
            return False
        if normalized_current == cls.ADMINISTRATOR_ROLE:
            return True
        return normalized_current == normalized_required

    @classmethod
    def has_any_role(cls, current_role: Any, required_roles: Iterable[str]) -> bool:
        return any(cls.has_role(current_role, required_role) for required_role in required_roles)