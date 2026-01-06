from fastapi import APIRouter

from .views import router as health_router

router = APIRouter(tags=["Health"])
router.include_router(health_router)