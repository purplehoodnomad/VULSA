from abc import ABC, abstractmethod

from src.domain.repositories.abstract import AbstractRepository
from .entity import Link
from ..common.value_objects import LinkId
from .value_objects import Short


class AbstractLinkRepository(AbstractRepository[Link, LinkId], ABC):
    @abstractmethod
    async def get_by_short(self, short: Short) -> Link:
        raise NotImplementedError
    
    # @abstractmethod
    # async def get_user_links(self, owner_id: UUID) -> list[LinkDTO]:
    #     raise NotImplementedError
    
    # @abstractmethod
    # async def get_all_expired(self, owner_id: UUID) -> list[LinkDTO]:
    #     raise NotImplementedError