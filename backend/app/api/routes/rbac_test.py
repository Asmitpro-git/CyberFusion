from fastapi import APIRouter

from app.auth.dependencies import CurrentUser
from app.rbac.decorators import require_permission, require_role

router = APIRouter(
    prefix="/rbac-test",
    tags=["RBAC Test"],
)


@router.get("/admin")
@require_role("Administrator")
def admin_only(
    current_user: CurrentUser,
) -> dict[str, str]:
    return {
        "message": "Administrator access granted.",
    }


@router.get("/dashboard")
@require_permission("dashboard:view")
def dashboard_access(
    current_user: CurrentUser,
) -> dict[str, str]:
    return {
        "message": "Dashboard permission granted.",
    }