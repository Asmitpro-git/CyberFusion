from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

ROLE_ATTRIBUTE = "__rbac_required_roles__"
PERMISSION_ATTRIBUTE = "__rbac_required_permissions__"


def _attach_requirement(target: Callable[..., Any], attribute_name: str, value: str) -> Callable[..., Any]:
    existing_values = list(getattr(target, attribute_name, []))
    if value not in existing_values:
        existing_values.append(value)
    setattr(target, attribute_name, tuple(existing_values))
    return target


def require_role(required_role: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        _attach_requirement(func, ROLE_ATTRIBUTE, required_role)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return func(*args, **kwargs)

        setattr(wrapper, ROLE_ATTRIBUTE, getattr(func, ROLE_ATTRIBUTE, (required_role,)))
        setattr(wrapper, PERMISSION_ATTRIBUTE, getattr(func, PERMISSION_ATTRIBUTE, ()))
        return wrapper

    return decorator


def require_permission(required_permission: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        _attach_requirement(func, PERMISSION_ATTRIBUTE, required_permission)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return func(*args, **kwargs)

        setattr(wrapper, ROLE_ATTRIBUTE, getattr(func, ROLE_ATTRIBUTE, ()))
        setattr(wrapper, PERMISSION_ATTRIBUTE, getattr(func, PERMISSION_ATTRIBUTE, (required_permission,)))
        return wrapper

    return decorator