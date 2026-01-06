from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Request
import asyncpg


router = APIRouter(prefix="/health")


@router.get("/live")
async def liveness_probe() -> dict[str, Any]:
    """Checks API health."""
    return {
        "status": "UP",
        "timestamp": datetime.now(timezone.utc),
    }


async def check_db(pool: asyncpg.Pool) -> bool:
    async with pool.acquire() as conn:
        await conn.execute("SELECT 1")
    return True

@router.get("/ready")
async def readiness_probe(request: Request) -> dict[str, Any]:
    """Checks DB connection."""
    pool = request.app.state.db_pool
    try:
        await check_db(pool)
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