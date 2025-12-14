from fastapi import APIRouter

from .link import routers as link_router
from .user import routers as user_router

router = APIRouter(prefix="/api/v1")
router.include_router(link_router.router)
router.include_router(user_router.router)