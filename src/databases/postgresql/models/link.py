from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy import UUID as UUIDAlchemy

from ..base import Base

class Link(Base):
    __tablename__ = "link"

    owner_id: Mapped[Optional[UUID]] = mapped_column(UUIDAlchemy)
    url_id: Mapped[UUID] = mapped_column(UUIDAlchemy, primary_key=True)
    base_url: Mapped[str] = mapped_column(String(2048))
    suffix: Mapped[str] = mapped_column(String(16))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    redirect_limit: Mapped[Optional[int]] = mapped_column(Integer())
    times_used: Mapped[int] = mapped_column(Integer())
    is_active: Mapped[bool] = mapped_column(Boolean())

    # @dataclass(slots=True)
    # class Link:
    #     owner_id: UUID | None
    #     url_id: UUID
    #     base_url: str
    #     # short_url: str
    #     suffix: str
    #     expires_at: Optional[datetime]
    #     redirect_limit: Optional[int]
    #     times_used: int
    #     is_active: bool