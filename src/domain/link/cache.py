from abc import ABC, abstractmethod
from typing import Optional

from infrastructure.cache.entries.link import LinkCacheEntry


class AbstractLinkCache(ABC):
    @abstractmethod
    async def save(self, entry: LinkCacheEntry, ttl: Optional[int] = None) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def get(self, short: str) -> LinkCacheEntry:
        raise NotImplementedError()

    @abstractmethod
    async def get_and_increment(self, short: str) -> LinkCacheEntry:
        raise NotImplementedError()