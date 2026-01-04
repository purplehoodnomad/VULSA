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
            entity = dto.to_entity()
            link = await uow.link_repo.create(entity)
            return LinkDTO.from_entity(link)