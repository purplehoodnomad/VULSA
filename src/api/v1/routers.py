from fastapi import APIRouter

from .link import routers as link_router
from .user import routers as user_router
from .auth import routers as auth_router
from .health import routers as health_router


router = APIRouter(prefix="/api/v1")
router.include_router(health_router.router)
router.include_router(auth_router.router)
router.include_router(user_router.router)
router.include_router(link_router.router)