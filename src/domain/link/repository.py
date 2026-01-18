from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from domain.repositories.abstract import AbstractRepository

from domain.value_objects.link import Short, AnonymousEditKey
from domain.value_objects.common import UserId

from .entity import Link


class AbstractLinkRepository(AbstractRepository[Link], ABC):
    @abstractmethod
    async def get_by_short(self, short: Short) -> Link:
        raise NotImplementedError

    @abstractmethod
    async def get_by_edit_key(self, edit_key: AnonymousEditKey) -> Link:
        raise NotImplementedError
    
    @abstractmethod
    async def is_short_taken(self, short: Short) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def list(self,
        *,
        offset: int,
        limit: int,
        user_id: Optional[UserId] = None,
        edit_key: Optional[AnonymousEditKey] = None,
        older_than: Optional[datetime] = None,
        newer_than: Optional[datetime] = None,
        active_status: Optional[bool] = None,
        has_expiration_date: Optional[bool] = None,
        has_redirect_limit: Optional[bool] = None,
    ) -> list[Link]:
        raise NotImplementedError