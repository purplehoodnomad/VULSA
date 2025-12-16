from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import UUID

from domain.repositories.abstract import AbstractRepository
from domain.value_objects.common import LinkId
from domain.value_objects.link import Short

from .entity import Link


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