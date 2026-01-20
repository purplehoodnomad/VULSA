from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from infrastructure.sqlalchemy.session import get_async_connection


router = APIRouter(prefix="/health")


@router.get("/live")
async def liveness_probe() -> dict[str, Any]:
    """Checks API health."""
    return {
        "status": "UP",
        "timestamp": datetime.now(timezone.utc),
    }


@router.get("/ready")
async def readiness_probe(connection: AsyncConnection = Depends(get_async_connection)) -> dict[str, Any]:
    """Checks DB connection."""
    try:
        await connection.execute(text("SELECT 1"))
        return {
            "status": "UP",
            "checks": {
                "database": {"status": "UP"},
                "service": {"status": "UP"},
            },
            "timestamp": datetime.now(timezone.utc),
        }
    except Exception as e:
        print(e)
        return {
            "status": "DOWN",
            "checks": {
                "database": {"status": "DOWN"},
                "service": {"status": "UP"},
            },
            "timestamp": datetime.now(timezone.utc),
        }