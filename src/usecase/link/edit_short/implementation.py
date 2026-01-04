from uuid import UUID

from infrastructure.uow.link import AbstractLinkUnitOfWork

from domain.value_objects.common import UserId
from domain.value_objects.link import Long, Short, RedirectLimit

from domain.link.exceptions import ShortLinkAlreadyExists, ShortLinkAccessDenied

from usecase.link.utils.dto import LinkDTO, LinkUpdateDTO

from .abstract import AbstractEditShortLinkUseCase


class PostgresEditShortLinkUseCase(AbstractEditShortLinkUseCase):
    def __init__(self, uow: AbstractLinkUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        *,
        user_id: UUID,
        short: str,
        dto: LinkUpdateDTO
    ) -> LinkDTO:
        async with self.uow as uow:
            user = await uow.user_repo.get(UserId(user_id))
            link = await uow.link_repo.get_by_short(Short(short))
            if link.user_id.value != user.user_id.value:
                raise ShortLinkAccessDenied()
            
            if dto.long is not None:
                link.change_long(Long(dto.long))
            
            if dto.new_short is not None:
                if await uow.link_repo.is_short_taken(Short(dto.new_short)):
                    raise ShortLinkAlreadyExists()
                
                link.change_short(Short(dto.new_short))
            
            if dto.expires_at is not None:
                link.change_expiration_date(dto.expires_at)
            
            if dto.redirect_limit is not None:
                link.change_redirect_limit(RedirectLimit(dto.redirect_limit))
            
            if dto.is_active is not None:
                link.activate() if dto.is_active else link.deactivate()
            
            updated_link = await uow.link_repo.update(link)
            return LinkDTO.from_entity(updated_link)