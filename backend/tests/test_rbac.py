from __future__ import annotations

import unittest
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.auth.dependencies import AuthenticatedUser
from app.middleware.authorization import AuthorizationMiddleware
from app.models.role import Role
from app.rbac.decorators import PERMISSION_ATTRIBUTE, ROLE_ATTRIBUTE, require_permission, require_role
from app.rbac.dependencies import require_permission_dependency, require_role_dependency
from app.rbac.engine import PermissionEngine, RoleEngine


def build_role(name: str, permissions: dict[str, object]) -> Role:
    role = Role(name=name, description=f"{name} role", permissions=permissions)
    role.id = uuid4()
    role.created_at = datetime.now(UTC)
    return role


def build_user(role: Role, *, active: bool = True) -> AuthenticatedUser:
    now = datetime.now(UTC)
    return AuthenticatedUser(
        id=uuid4(),
        username="analyst",
        email="analyst@example.com",
        role=role,
        permissions=dict(role.permissions),
        is_active=active,
        is_verified=True,
        failed_login_attempts=0,
        locked_until=None,
        last_login=now,
        created_at=now,
        updated_at=now,
    )


class PermissionEngineTests(unittest.TestCase):
    def test_normalize_accepts_nested_and_flat_permissions(self) -> None:
        nested = {"alerts": {"update": True}, "dashboard:view": True}
        flat = ["alerts:update", "dashboard:view"]

        self.assertTrue(PermissionEngine.has_permissions(nested, ["alerts:update", "dashboard:view"]))
        self.assertTrue(PermissionEngine.has_permissions(flat, ["alerts:update", "dashboard:view"]))


class RoleEngineTests(unittest.TestCase):
    def test_administrator_has_all_roles(self) -> None:
        self.assertTrue(RoleEngine.has_role("Administrator", "Viewer"))
        self.assertTrue(RoleEngine.has_any_role("Administrator", ["Viewer", "SOC Analyst"]))

    def test_non_admin_requires_exact_match(self) -> None:
        self.assertTrue(RoleEngine.has_role("SOC Analyst", "SOC Analyst"))
        self.assertFalse(RoleEngine.has_role("Viewer", "SOC Analyst"))


class DecoratorTests(unittest.TestCase):
    def test_metadata_is_attached(self) -> None:
        @require_role("Administrator")
        @require_permission("alerts:update")
        def endpoint() -> str:
            return "ok"

        self.assertEqual(getattr(endpoint, ROLE_ATTRIBUTE), ("Administrator",))
        self.assertEqual(getattr(endpoint, PERMISSION_ATTRIBUTE), ("alerts:update",))


class DependencyTests(unittest.TestCase):
    def test_permission_dependency_allows_authorized_user(self) -> None:
        dependency = require_permission_dependency("alerts:update")
        user = build_user(build_role("SOC Analyst", {"alerts:update": True}))
        self.assertIs(dependency(current_user=user), user)

    def test_role_dependency_blocks_unauthorized_user(self) -> None:
        dependency = require_role_dependency("Administrator")
        user = build_user(build_role("Viewer", {"dashboard:view": True}))
        with self.assertRaises(Exception):
            dependency(current_user=user)


class MiddlewareTests(unittest.TestCase):
    def test_authorization_middleware_allows_protected_route(self) -> None:
        app = FastAPI()

        @app.get("/secure")
        @require_permission("alerts:update")
        def secure_route() -> dict[str, str]:
            return {"status": "ok"}

        app.add_middleware(AuthorizationMiddleware)

        role = build_role("SOC Analyst", {"alerts:update": True, "dashboard:view": True})
        user = build_user(role)

        class FakeSession:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def close(self) -> None:
                pass

        class FakeRepository:
            def __init__(self, session: FakeSession) -> None:
                self.session = session

            def get_with_role_by_id(self, user_id):
                return SimpleNamespace(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    role=role,
                    is_active=True,
                    is_verified=True,
                    failed_login_attempts=0,
                    locked_until=None,
                    last_login=user.last_login,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                )

        with patch("app.middleware.authorization.verify_token", return_value={"user_id": str(user.id), "token_type": "access"}), patch(
            "app.middleware.authorization.SessionLocal", return_value=FakeSession()
        ), patch("app.middleware.authorization.UserRepository", FakeRepository):
            with TestClient(app) as client:
                response = client.get("/secure", headers={"Authorization": "Bearer token"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_authorization_middleware_blocks_missing_permission(self) -> None:
        app = FastAPI()

        @app.get("/secure")
        @require_permission("alerts:delete")
        def secure_route() -> dict[str, str]:
            return {"status": "ok"}

        app.add_middleware(AuthorizationMiddleware)

        role = build_role("SOC Analyst", {"alerts:update": True})
        user = build_user(role)

        class FakeSession:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def close(self) -> None:
                pass

        class FakeRepository:
            def __init__(self, session: FakeSession) -> None:
                self.session = session

            def get_with_role_by_id(self, user_id):
                return SimpleNamespace(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    role=role,
                    is_active=True,
                    is_verified=True,
                    failed_login_attempts=0,
                    locked_until=None,
                    last_login=user.last_login,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                )

        with patch("app.middleware.authorization.verify_token", return_value={"user_id": str(user.id), "token_type": "access"}), patch(
            "app.middleware.authorization.SessionLocal", return_value=FakeSession()
        ), patch("app.middleware.authorization.UserRepository", FakeRepository):
            with TestClient(app) as client:
                response = client.get("/secure", headers={"Authorization": "Bearer token"})

        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()