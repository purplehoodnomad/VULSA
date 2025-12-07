from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.repositories.abstract import AbstractRepository
from .entity import Link
from ..common.value_objects import LinkId


class AbstractLinkRepository(AbstractRepository[Link, LinkId], ABC):
    # @abstractmethod
    # async def get_by_suffix(self, short_url: str) -> LinkDTO:
    #     raise NotImplementedError
    
    # @abstractmethod
    # async def get_user_links(self, owner_id: UUID) -> list[LinkDTO]:
    #     raise NotImplementedError
    
    # @abstractmethod
    # async def get_all_expired(self, owner_id: UUID) -> list[LinkDTO]:
    #     raise NotImplementedError
    ...