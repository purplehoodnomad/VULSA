from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import UUID

from domain.link.entity import Link
from domain.value_objects.common import UserId
from domain.value_objects.link import Short, Long, RedirectLimit


@dataclass(slots=True)
class LinkDTO:
    link_id: UUID
    user_id: UUID
    long: str
    short: str
    redirect_limit: Optional[int]
    expires_at: Optional[datetime]
    created_at: datetime
    times_used: int
    is_active: bool

    @staticmethod
    def from_entity(entity: Link):
        return LinkDTO(
            link_id=entity.link_id.value,
            user_id=entity.user_id.value,
            long=entity.long.value,
            short=entity.short.value,
            redirect_limit=entity.redirect_limit.value if entity.redirect_limit is not None else None,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
            times_used=entity.times_used,
            is_active=entity.is_active
        )


@dataclass(slots=True)
class LinkCreateDTO:
    user_id: UUID
    long: str
    short: Optional[str]
    expires_at: Optional[datetime]
    redirect_limit: Optional[int]

    def to_entity(self):
        "Converts dto into User entity with empty hashed password and USER status"
        return Link.create(
                user_id=UserId(self.user_id),
                long=Long(self.long),
                short=Short(self.short) if self.short else None,
                expires_at=self.expires_at,
                redirect_limit=RedirectLimit(self.redirect_limit)
            )


@dataclass(slots=True)
class LinkUpdateDTO:
    long: Optional[str] = None
    new_short: Optional[str] = None
    expires_at: Optional[datetime] = None
    redirect_limit: Optional[int] = None
    is_active: Optional[bool] = None


@dataclass(slots=True)
class LinkFilterDto:
    offset: int
    limit: int
    user: Optional[UUID] = None
    older_than: Optional[datetime] = None
    newer_than: Optional[datetime] = None
    active_status: Optional[bool] = None
    has_expiration_date: Optional[bool] = None
    has_redirect_limit: Optional[bool] = None