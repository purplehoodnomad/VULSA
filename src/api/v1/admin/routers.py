from fastapi import APIRouter

from .views import router as admin_router

router = APIRouter(tags=["Admin"])
router.include_router(admin_router)