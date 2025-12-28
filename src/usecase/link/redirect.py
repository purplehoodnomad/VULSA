from abc import ABC, abstractmethod

from infrastructure.repositories.postgresql.uow import PostgresLinkUoW
from domain.value_objects.link import Short

from usecase.link.utils.dto import LinkDTO


class AbstractLinkRedirectUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        short: str
    ) -> LinkDTO:
        raise NotImplementedError


class PostgresLinkRedirectUseCase(AbstractLinkRedirectUseCase):
    def __init__(self, uow: PostgresLinkUoW):
        self.uow = uow

    async def execute(
        self,
        short: str
    ) -> LinkDTO:
        async with self.uow as uow:
            link = await uow.repository.get_by_short(Short(short)) # type: ignore
            link.consume_redirect()
            redirected_link = await uow.repository.update(link) # type: ignore
            return LinkDTO.from_entity(redirected_link)