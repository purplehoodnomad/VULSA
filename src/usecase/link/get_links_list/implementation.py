from infrastructure.uow.link import AbstractLinkUnitOfWork

from domain.value_objects.common import UserId

from usecase.link.utils.dto import LinkDTO, LinkFilterDto

from .abstract import AbstractGetLinksListUseCase


class PostgresGetLinksListUseCase(AbstractGetLinksListUseCase):
    def __init__(self, uow: AbstractLinkUnitOfWork):
        self.uow = uow
    
    async def execute(self, dto: LinkFilterDto) -> list[LinkDTO]:
        async with self.uow as uow:
            links = await uow.link_repo.list(
                offset=dto.offset,
                limit=dto.limit,
                user_id=UserId(dto.user) if dto.user is not None else None,
                older_than=dto.older_than,
                newer_than=dto.newer_than,
                active_status=dto.active_status,
                has_expiration_date=dto.has_expiration_date,
                has_redirect_limit=dto.has_redirect_limit,
            )
            
            return [LinkDTO.from_entity(link) for link in links]