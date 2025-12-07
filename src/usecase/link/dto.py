from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Link:
    link_id: UUID
    user_id: UUID
    long: str
    short: str
    redirect_limit: Optional[int]
    expires_at: Optional[datetime]
    created_at: datetime
    times_used: int
    is_active: bool



@dataclass(slots=True)
class LinkCreateDTO:
    user_id: UUID
    long: str
    short: Optional[str]
    expires_at: Optional[datetime]
    redirect_limit: Optional[int]


# @dataclass(slots=True)
# class LinkUpdate:
#     url_id: Optional[UUID] = None
#     is_active: Optional[bool] = None
#     user_id: Optional[UUID] = None
#     expires_at: Optional[datetime] = None
#     redirect_limit: Optional[int] = None
#     times_used: Optional[int] = None

