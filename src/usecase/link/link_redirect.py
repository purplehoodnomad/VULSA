from abc import ABC, abstractmethod

from infrastructure.repositories.postgresql.uow import PostgreSQLLinkUoW

from domain.link.value_objects import Short

from .mappers import to_schema
from api.v1.link.schemas import LinkSchema


class LinkRedirectUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        short: str
    ) -> LinkSchema:
        raise NotImplementedError


class LinkRedirectUseCaseImpl(LinkRedirectUseCase):
    def __init__(self, uow: PostgreSQLLinkUoW):
        self.uow = uow

    async def execute(
        self,
        short: str
    ) -> LinkSchema:
        async with self.uow as uow:
            if uow.repository is not None:
                link = await uow.repository.get_by_short(Short(short))
                return to_schema(link)
            
            raise Exception("No repository for UoW")