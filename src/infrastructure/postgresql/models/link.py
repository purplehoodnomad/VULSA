from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy import UUID as UUIDAlchemy

from infrastructure.sqlalchemy.base import Base

from domain.link.entity import Link
from domain.value_objects.common import (
    LinkId,
    UserId
)
from domain.value_objects.link import (
    Long,
    Short,
    RedirectLimit
)


class LinkORM(Base):
    __tablename__ = "link"

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="links", passive_deletes=True) # type: ignore
    clicks: Mapped[list["ClickStampORM"]] = relationship(back_populates="link", cascade="all, delete, delete-orphan") # type: ignore

    user_id: Mapped[UUID] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        ForeignKey('user.id', ondelete="CASCADE"),
        nullable=False
    )
    
    id: Mapped[UUID] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    
    long: Mapped[str] = mapped_column(
        String(2048),
        nullable=False
    )

    short: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        index=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=True
    )

    times_used: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
        default=0
    )
    
    redirect_limit: Mapped[Optional[int]] = mapped_column(Integer())
    
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    @staticmethod
    def from_entity(link: Link) -> "LinkORM":
        return LinkORM(
            id=link.link_id.value,
            user_id=link.user_id.value,
            long=link.long.value,
            short=link.short.value,
            redirect_limit=link.redirect_limit.value if link.redirect_limit is not None else None,
            expires_at=link.expires_at,
            created_at=link.created_at,
            times_used=link.times_used,
            is_active=link.is_active
        )
    
    def to_entity(self):
        return Link(
            link_id=LinkId(self.id),
            user_id=UserId(self.user_id),
            long=Long(self.long),
            short=Short(self.short),
            redirect_limit=RedirectLimit(self.redirect_limit),
            expires_at=self.expires_at,
            created_at=self.created_at,
            times_used=self.times_used,
            is_active=self.is_active
        )