from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy import UUID as UUIDAlchemy

from ..base import Base

from domain.link.entity import Link
from domain.common.value_objects import (
    LinkId,
    UserId
)
from domain.link.value_objects import (
    Long,
    Short,
    RedirectLimit
)


class LinkORM(Base):
    __tablename__ = "link"

    user_id: Mapped[UUID] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        # ForeignKey('user.id'),
        nullable=False
    )
    
    id: Mapped[UUID] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        primary_key=True,
        nullable=False,
        # default=uuid4 # вызывает метод до SQL
    )
    
    long: Mapped[str] = mapped_column(
        String(2048),
        nullable=False
    )

    short: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        index=True # ускоряет SELECT, но замедляет INSERT и UPDATE
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
        # server_default=func.now() # подсовывает now() в SQL
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
            redirect_limit=RedirectLimit(self.redirect_limit) if self.redirect_limit is not None else None,
            expires_at=self.expires_at,
            created_at=self.created_at,
            times_used=self.times_used,
            is_active=self.is_active
        )
    
    # user: Mapped["User"] = relationship("User", back_populates="links") # атрибут связи, обещаем клас User и links как поле в нем