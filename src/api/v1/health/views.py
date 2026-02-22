from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from infrastructure.sqlalchemy.session import get_async_connection
from infrastructure.cache.redis.client import RedisClient
from infrastructure.cache.redis.dependencies import get_redis_client
from infrastructure.broker.kafka.client import KafkaClient
from infrastructure.broker.kafka.dependencies import get_kafka_client
from infrastructure.clickhouse.client import ClickHouseClient
from infrastructure.clickhouse.dependencies import get_clickhouse_client


router = APIRouter(prefix="/health")


@router.get("/live")
async def live() -> dict[str, Any]:
    """Checks API health."""
    return {
        "status": "UP",
        "timestamp": datetime.now(timezone.utc),
    }


@router.get("/ready")
async def ready(
    postgres_connection: AsyncConnection = Depends(get_async_connection),
    redis: RedisClient = Depends(get_redis_client),
    kafka: KafkaClient = Depends(get_kafka_client),
    clickhouse: ClickHouseClient = Depends(get_clickhouse_client)
) -> dict[str, Any]:
    """Checks all connections."""
    checks = {}
    checks["api"] = {"status": "UP"}

    # Postgres connection
    try:
        await postgres_connection.execute(text("SELECT 1"))
        checks["database"] = {"status": "UP"}
    except Exception:
        checks["database"] = {"status": "DOWN"}
    
    # Redis connection
    try:
        pong = await redis.client.ping() # type: ignore
        if pong:
            checks["redis"] = {"status": "UP"}
        else:
            checks["redis"] = {"status": "DOWN"}
    except Exception:
        checks["redis"] = {"status": "DOWN"}
    
    # Kafka connection
    try:
        await kafka.get_producer()
        checks["kafka"] = {"status": "UP"}
    except Exception:
        checks["kafka"] = {"status": "DOWN"}
    
    # ClickHouse connection
    try:
        with clickhouse.connect() as connection:
            connection.execute(text("SELECT 1"))
            checks["clickhouse"] = {"status": "UP"}
    except Exception:
        checks["clickhouse"] = {"status": "DOWN"}
    
    return {
        "checks": checks,
        "timestamp": datetime.now(timezone.utc),
    }