from fastapi import APIRouter

from .views import router as redirect_router

router = APIRouter(tags=["Redirect"])
router.include_router(redirect_router)