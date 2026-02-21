from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from container import Container
from infrastructure.clickhouse.client import ClickHouseClient


@inject
async def get_clickhouse_client(
    ch_client: ClickHouseClient = Depends(Provide[Container.clickhouse_client])
) -> ClickHouseClient:
    return ch_client