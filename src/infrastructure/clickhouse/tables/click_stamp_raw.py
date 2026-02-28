from clickhouse_sqlalchemy import engines
from sqlalchemy import Column, String, DateTime, UUID, text

from infrastructure.sqlalchemy.base import Base
from domain.value_objects.link import ClickStamp


class ClickStampCH(Base):
    __tablename__ = "click_stamp"
    __table_args__ = (
        engines.MergeTree(
            partition_by=text("toYYYYMM(timestamp)"),
            order_by=("link_id", "timestamp", "id"),
        ),
        {"extend_existing": True}
    )

    id = Column(UUID, primary_key=True)
    link_id = Column(UUID)
    short = Column(String(128))
    timestamp = Column(DateTime)
    
    geo = Column(String)
    platform = Column(String)
    client = Column(String)

    @staticmethod
    def entity_to_row(entity: ClickStamp) -> dict:
        return {
            "id": entity.id.value,
            "link_id": entity.link_id.value,
            "short": entity.short.value,
            "timestamp": entity.timestamp,
            "user_agent": entity.user_agent,
            "referer": entity.referer,
            "geo": entity.geo,
            "platform": entity.platform,
            "client": entity.client
        }