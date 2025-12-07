from fastapi import APIRouter

from .views import router as owner_router

router = APIRouter(tags=["Owner"])
router.include_router(owner_router)