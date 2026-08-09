from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.rbac_test import router as rbac_test_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(rbac_test_router)