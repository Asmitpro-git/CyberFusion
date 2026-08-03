from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.auth.dependencies import AuthenticatedUser, CurrentUser, get_current_user
from app.rbac.engine import PermissionEngine, RoleEngine


def get_current_role(current_user: CurrentUser = Depends(get_current_user)) -> str:
    return current_user.role.name


def get_current_permissions(current_user: CurrentUser = Depends(get_current_user)) -> set[str]:
    return PermissionEngine.normalize(current_user.permissions)


def _forbidden(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def require_role_dependency(required_role: str):
    def dependency(current_user: CurrentUser = Depends(get_current_user)) -> AuthenticatedUser:
        if not RoleEngine.has_role(current_user.role.name, required_role):
            raise _forbidden("Insufficient role privileges")
        return current_user

    return dependency


def require_permission_dependency(required_permission: str):
    def dependency(current_user: CurrentUser = Depends(get_current_user)) -> AuthenticatedUser:
        if not PermissionEngine.has_permission(current_user.permissions, required_permission):
            raise _forbidden("Insufficient permission privileges")
        return current_user

    return dependency


CurrentRoleName = Annotated[str, Depends(get_current_role)]
CurrentPermissionSet = Annotated[set[str], Depends(get_current_permissions)]