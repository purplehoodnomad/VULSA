from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Link:
    owner_id: UUID | None
    url_id: UUID
    base_url: str
    # short_url: str
    suffix: str
    expires_at: Optional[datetime]
    redirect_limit: Optional[int]
    times_used: int
    is_active: bool

    def consume_redirect(self):
        self.times_used += 1
        if self.redirect_limit is not None and self.times_used >= self.redirect_limit:
            self.is_active = False
        return LinkUpdateDTO(
            is_active=self.is_active,
            times_used=self.times_used
        )

@dataclass(slots=True)
class LinkCreateDTO:
    owner_id: UUID | None
    base_url: str
    expires_at: Optional[datetime]
    redirect_limit: Optional[int]


@dataclass(slots=True)
class LinkUpdateDTO:
    is_active: Optional[bool] = None
    owner_id: Optional[UUID] = None
    expires_at: Optional[datetime] = None
    redirect_limit: Optional[int] = None
    times_used: Optional[int] = None