from abc import ABC, abstractmethod

from domain.repositories.abstract import AbstractRepository
from domain.value_objects.common import LinkId
from domain.value_objects.link import Short

from .entity import Link


class AbstractLinkRepository(AbstractRepository[Link, LinkId], ABC):
    @abstractmethod
    async def get_by_short(self, short: Short) -> Link:
        raise NotImplementedError