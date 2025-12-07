from fastapi import APIRouter

from .link import routers as link_router
# from .owner import routers as owner_router

router = APIRouter(prefix="/api/v1")
router.include_router(link_router.router)
# router.include_router(owner_router.router)