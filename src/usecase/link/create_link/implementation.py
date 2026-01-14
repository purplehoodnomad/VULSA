from usecase.link.utils.dto import LinkDTO, LinkCreateDTO

from infrastructure.uow.link import AbstractLinkUnitOfWork

from .abstract import AbstractCreateLinkUseCase


class PostgresCreateLinkUseCase(AbstractCreateLinkUseCase):
    def __init__(self, uow: AbstractLinkUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        dto: LinkCreateDTO
    ) -> LinkDTO:
        async with self.uow as uow:
            link = dto.to_entity()
            await uow.link_repo.create(link)
            return LinkDTO.from_entity(link)