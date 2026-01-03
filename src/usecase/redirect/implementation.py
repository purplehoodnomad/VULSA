from infrastructure.uow.link import AbstractLinkUnitOfWork
from domain.value_objects.link import Short

from usecase.link.utils.dto import LinkDTO

from .abstract import AbstractLinkRedirectUseCase


class PostgresLinkRedirectUseCase(AbstractLinkRedirectUseCase):
    def __init__(self, uow: AbstractLinkUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        short: str
    ) -> LinkDTO:
        async with self.uow as uow:
            link = await uow.link_repo.get_by_short(Short(short)) # type: ignore
            link.consume_redirect()
            redirected_link = await uow.link_repo.update(link) # type: ignore
            return LinkDTO.from_entity(redirected_link)