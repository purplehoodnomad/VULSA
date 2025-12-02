from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.repositories.abstract import AbstractRepository
from .schemas import Link, LinkCreateDTO, LinkUpdateDTO


class AbstractLinkRepository(AbstractRepository[Link, UUID, LinkCreateDTO, LinkUpdateDTO], ABC):
    @abstractmethod
    def _generate_suffix(self, dto: LinkCreateDTO | LinkUpdateDTO) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_suffix(self, short_url: str) -> Link:
        raise NotImplementedError
    
    @abstractmethod
    def get_user_links(self, owner_id: UUID) -> list[Link]:
        raise NotImplementedError
    
    @abstractmethod
    def get_all_expired(self, owner_id: UUID) -> list[Link]:
        raise NotImplementedError
    
    @abstractmethod
    def is_owner(self, url_id: UUID, owner_id: UUID) -> bool:
        raise NotImplementedError