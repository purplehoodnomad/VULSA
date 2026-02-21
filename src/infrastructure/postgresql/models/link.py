from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy import UUID as UUIDAlchemy

from infrastructure.sqlalchemy.base import Base

from domain.link.entity import Link
from domain.value_objects.common import LinkId, UserId
from domain.value_objects.link import (
    Long,
    Short,
    RedirectLimit,
    AnonymousEditKey
)


class LinkORM(Base):
    __tablename__ = "link"
    __table_args__ = (
        CheckConstraint(
            'NOT (user_id IS NULL AND edit_key IS NULL)',
            name='user_or_edit_key_required'
        ),
    )

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="links", passive_deletes=True) # type: ignore
    # clicks: Mapped[list["ClickStampORM"]] = relationship(back_populates="link", cascade="all, delete, delete-orphan") # type: ignore


    id: Mapped[UUID] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    user_id: Mapped[Optional[UUID]] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
    )

    edit_key: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True
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

    last_used: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


    @staticmethod
    def from_entity(entity: Link) -> "LinkORM":
        return LinkORM(
            id=entity.link_id.value,
            user_id=entity.owner_id.value if isinstance(entity.owner_id, UserId) else None,
            edit_key=entity.owner_id.value if isinstance(entity.owner_id, AnonymousEditKey) else None,
            long=entity.long.value,
            short=entity.short.value,
            redirect_limit=entity.redirect_limit.value if entity.redirect_limit is not None else None,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
            times_used=entity.times_used,
            is_active=entity.is_active,
            last_used=entity.last_used
        )
    
    def to_entity(self) -> Link:
        return Link(
            link_id=LinkId(self.id),
            owner_id=UserId(self.user_id) if self.user_id is not None else AnonymousEditKey(self.edit_key), # type: ignore
            long=Long(self.long),
            short=Short(self.short),
            redirect_limit=RedirectLimit(self.redirect_limit),
            expires_at=self.expires_at,
            created_at=self.created_at,
            times_used=self.times_used,
            is_active=self.is_active,
            last_used=self.last_used
        )
    
    def update_from_entity(self, entity: Link):
        self.user_id = entity.owner_id.value if isinstance(entity.owner_id, UserId) else None
        self.edit_key = entity.owner_id.value if isinstance(entity.owner_id, AnonymousEditKey) else None
        self.long = entity.long.value
        self.short = entity.short.value
        self.is_active = entity.is_active
        self.redirect_limit = entity.redirect_limit.value if entity.redirect_limit is not None else None
        self.expires_at = entity.expires_at
        self.times_used = entity.times_used
        self.last_used = entity.last_used