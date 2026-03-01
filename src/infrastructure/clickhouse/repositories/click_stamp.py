from typing import Iterable
from sqlalchemy import insert, text
from datetime import datetime

from domain.link.entity import Link
from infrastructure.clickhouse.client import ClickHouseClient
from infrastructure.clickhouse.tables import ClickStampCH

from domain.link.repository import AbstractClickStampRepository
from domain.value_objects.link import ClickStamp
from usecase.link.utils.dto import LinkClientStatsDTO, LinkGeoStatsDTO, LinkTimeStatsDTO


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
        stmt = insert(ClickStampCH)
        with self._client.connect() as conn:
            conn.execute(stmt, rows)
    
    async def truncate_raw(self) -> None:
        with self._client.connect() as conn:
            stmt = text(f"TRUNCATE TABLE IF EXISTS {ClickStampCH.__tablename__}")
            conn.execute(stmt)


    async def get_link_stats_by_time(self, link: Link) -> LinkTimeStatsDTO:
        stmt = text("""
            SELECT
                link_id,
                date,
                hour,
                countMerge(clicks_count) AS clicks_count
            FROM clicks_by_date
            WHERE link_id = :link_id
            GROUP BY link_id, date, hour
            ORDER BY date, hour
        """)
        with self._client.connect() as conn:
            res = conn.execute(stmt, {"link_id": str(link.link_id.value)})
            rows = res.fetchall()
        if not rows:
            return LinkTimeStatsDTO(link_id=link.link_id.value, stats={})
        
        stats: dict[str, dict[str, int]] = {}
        for row in rows:
            date = str(row.date)
            hour = str(row.hour)
            if date not in stats:
                stats[date] = {}
            stats[date][hour] = row.clicks_count

        return LinkTimeStatsDTO(
            link_id=link.link_id.value,
            stats=stats
        )
    
    async def get_link_stats_by_geo(self, link: Link) -> LinkGeoStatsDTO:
        stmt = text("""
            SELECT
                link_id,
                geo,
                countMerge(clicks_count) AS clicks_count
            FROM clicks_by_geo
            WHERE link_id = :link_id
            GROUP BY link_id, geo
            ORDER BY clicks_count
        """)
        with self._client.connect() as conn:
            res = conn.execute(stmt, {"link_id": str(link.link_id.value)})
            rows = res.fetchall()
        if not rows:
            return LinkGeoStatsDTO(link_id=link.link_id.value, stats={})

        stats: dict[str, int] = {}
        for row in rows:
            stats[row.geo] = row.clicks_count

        return LinkGeoStatsDTO(
            link_id=link.link_id.value,
            stats=stats
        )
    
    async def get_link_stats_by_client(self, link: Link) -> LinkClientStatsDTO:
        stmt = text("""
            SELECT
                link_id,
                platform,
                client,
                countMerge(clicks_count) AS clicks_count
            FROM clicks_by_client
            WHERE link_id = :link_id
            GROUP BY link_id, platform, client
            ORDER BY clicks_count
        """)
        with self._client.connect() as conn:
            res = conn.execute(stmt, {"link_id": str(link.link_id.value)})
            rows = res.fetchall()
        
        stats: dict[tuple[str, str], int] = {}
        for row in rows:
            stats[(row.platform, row.client)] = row.clicks_count
        if not rows:
            return LinkClientStatsDTO(link_id=link.link_id.value, stats={})

        return LinkClientStatsDTO(
            link_id=link.link_id.value,
            stats=stats
        )