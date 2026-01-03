from abc import ABC, abstractmethod

from infrastructure.postgresql.uow.uow import PostgresLinkUoW

from usecase.link.utils.dto import LinkDTO, LinkCreateDTO


class AbstractCreateLinkUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: LinkCreateDTO
    ) -> LinkDTO:
        raise NotImplementedError


class PostgresCreateLinkUseCase(AbstractCreateLinkUseCase):
    def __init__(self, uow: PostgresLinkUoW):
        self.uow = uow

    async def execute(
        self,
        dto: LinkCreateDTO
    ) -> LinkDTO:
        async with self.uow as uow:
            entity = dto.to_entity()
            from domain.value_objects.link import Short

            link = await uow.repository.create(entity) # type: ignore
            return LinkDTO.from_entity(link)