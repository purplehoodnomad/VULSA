from datetime import datetime, timezone
from typing import Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from sqlalchemy import text

from container import Container
from infrastructure.sqlalchemy.session_manager import DatabaseSessionManager


router = APIRouter(prefix="/health")


@router.get("/live")
async def liveness_probe() -> dict[str, Any]:
    """Checks API health."""
    return {
        "status": "UP",
        "timestamp": datetime.now(timezone.utc),
    }


@inject
@router.get("/ready")
async def readiness_probe(
    session_manager: DatabaseSessionManager = Depends(Provide[Container.session_manager])
) -> dict[str, Any]:
    """Checks DB connection."""
    try:
        async with session_manager.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {
            "status": "UP",
            "checks": {
                "database": {"status": "UP"},
                "service": {"status": "UP"},
            },
            "timestamp": datetime.now(timezone.utc),
        }
    except Exception as e:
        return {
            "status": "DOWN",
            "checks": {
                "database": {"status": "DOWN"},
                "service": {"status": "UP"},
            },
            "timestamp": datetime.now(timezone.utc),
        }