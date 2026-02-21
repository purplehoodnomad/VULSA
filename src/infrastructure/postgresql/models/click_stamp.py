from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy import UUID as UUIDAlchemy

from infrastructure.sqlalchemy.base import Base

from domain.value_objects.common import LinkId
from domain.value_objects.link import Short, ClickStamp, ClickStampId


class ClickStampORM(Base):
    __tablename__ = "click_stamp"
    __abstract__ = True

    # link: Mapped["LinkORM"] = relationship("LinkORM", back_populates="clicks", passive_deletes=True) # type: ignore

    id: Mapped[UUID] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    link_id: Mapped[UUID] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        # ForeignKey('link.id', ondelete="CASCADE"),
        nullable=False
    )

    short: Mapped[str] = mapped_column(String(128), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ip: Mapped[Optional[str]] = mapped_column(String(16))
    user_agent: Mapped[Optional[str]] = mapped_column(String(1024))
    referer: Mapped[Optional[str]] = mapped_column(String(2048))
    request_url: Mapped[Optional[str]] = mapped_column(String(2048))

    @staticmethod
    def from_entity(entity: ClickStamp) -> "ClickStampORM":
        return ClickStampORM(
            id=entity.id.value,
            link_id=entity.link_id.value,
            short=entity.short.value,
            timestamp=entity.timestamp,
            ip=entity.ip,
            user_agent=entity.user_agent,
            referer=entity.referer,
            request_url=entity.request_url
        )

    def to_entity(self):
        return ClickStamp(
            id=ClickStampId(self.id),
            link_id=LinkId(self.link_id),
            short=Short(self.short),
            timestamp=self.timestamp,
            ip=self.ip,
            user_agent=self.user_agent,
            referer=self.referer,
            request_url=self.request_url
        )