from dataclasses import dataclass
from typing import Optional

from domain.link.entity import Link


@dataclass
class LinkCacheEntry:
    short: str
    long: str
    expires_at: Optional[int]
    redirect_limit: Optional[int]
    times_used: int

    @staticmethod
    def from_entity(entity: Link) -> "LinkCacheEntry":
        return LinkCacheEntry(
            short=entity.short.value,
            long=entity.long.value,
            expires_at=int(entity.expires_at.timestamp()) if entity.expires_at is not None else None,
            redirect_limit=entity.redirect_limit.value,
            times_used=entity.times_used
        )