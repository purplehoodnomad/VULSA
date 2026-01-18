from usecase.link.utils.dto import LinkDTO


from infrastructure.uow.link import AbstractLinkUnitOfWork
from usecase.link.utils.dto import LinkDTO
from .abstract import AbstractGetAnonymousLinkUseCase
from domain.value_objects.link import AnonymousEditKey



class PostgresGetAnonymousLinkUseCase(AbstractGetAnonymousLinkUseCase):
    def __init__(self, uow: AbstractLinkUnitOfWork):
        self.uow = uow
    

    async def execute(self, edit_key: str) -> LinkDTO:
        async with self.uow as uow:
            link_entity = await uow.link_repo.get_by_edit_key(AnonymousEditKey(edit_key))

            return LinkDTO.from_entity(link_entity)