from typing import Iterable
from sqlalchemy import insert

from infrastructure.clickhouse.client import ClickHouseClient
from infrastructure.clickhouse.tables import ClickStampCH

from domain.link.repository import AbstractClickStampRepository
from domain.value_objects.link import ClickStamp


class ClickHouseClickStampRepository(AbstractClickStampRepository):
    def __init__(self, client: ClickHouseClient):
        self._client = client


    async def create(self, entity: ClickStamp) -> ClickStamp:
        row = ClickStampCH.entity_to_row(entity)
        with self._client.connect() as conn:
            conn.execute(insert(ClickStampCH), [row])
        return entity

    async def update(self, entity: ClickStamp) -> None:
        raise NotImplementedError("ClickHouse is immutable")

    async def delete(self, entity: ClickStamp) -> None:
        raise NotImplementedError("ClickHouse is immutable")

    async def create_batch(self, entities: Iterable[ClickStamp]) -> None:
        rows = [ClickStampCH.entity_to_row(e) for e in entities]
        if not rows:
            return
        with self._client.connect() as conn:
            conn.execute(insert(ClickStampCH), rows)