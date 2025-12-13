from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import UUID

from src.domain.repositories.abstract import AbstractRepository
from .entity import Link
from ..common.value_objects import LinkId
from .value_objects import Short


@dataclass(slots=True)
class LinkFilterDto:
    offset: int
    limit: int
    user: Optional[UUID]
    older_than: Optional[datetime]
    newer_than: Optional[datetime]
    active_status: Optional[bool]
    has_expiration_date: Optional[bool]
    has_redirect_limit: Optional[bool]


class AbstractLinkRepository(AbstractRepository[Link, LinkId, LinkFilterDto], ABC):
    @abstractmethod
    async def get_by_short(self, short: Short) -> Link:
        raise NotImplementedError
    
    # @abstractmethod
    # async def get_user_links(self, owner_id: UUID) -> list[LinkDTO]:
    #     raise NotImplementedError
    
    # @abstractmethod
    # async def get_all_expired(self, owner_id: UUID) -> list[LinkDTO]:
    #     raise NotImplementedError