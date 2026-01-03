from abc import ABC, abstractmethod
from uuid import UUID

from infrastructure.postgresql.uow.uow import PostgresLinkUoW

from domain.value_objects.common import UserId
from domain.value_objects.link import Long, Short, RedirectLimit

from domain.user.exceptions import LinkOwnershipViolation
from domain.link.exceptions import ShortLinkDoesNotExistException, ShortLinkAlreadyExistsException

from usecase.link.utils.dto import LinkDTO, LinkUpdateDTO


class AbstractEditShortLinkUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        *,
        user_id: UUID,
        short: str,
        dto: LinkUpdateDTO
    ) -> LinkDTO:
        raise NotImplementedError


class PostgresEditShortLinkUseCase(AbstractEditShortLinkUseCase):
    def __init__(self, uow: PostgresLinkUoW):
        self.uow = uow

    async def execute(
        self,
        *,
        user_id: UUID,
        short: str,
        dto: LinkUpdateDTO
    ) -> LinkDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get(UserId(user_id)) # type: ignore
            link = await uow.repository.get_by_short(Short(short)) # type: ignore
            if link.user_id.value != user.user_id.value:
                raise LinkOwnershipViolation(short=short, user_id=user_id)
            
            if dto.long is not None:
                link.change_long(Long(dto.long))
            
            if dto.new_short is not None:
                if await uow.repository.is_short_taken(Short(dto.new_short)): # type: ignore
                    raise ShortLinkAlreadyExistsException(short=dto.new_short)
                
                link.change_short(Short(dto.new_short))
            
            if dto.expires_at is not None:
                link.change_expiration_date(dto.expires_at)
            
            if dto.redirect_limit is not None:
                link.change_redirect_limit(RedirectLimit(dto.redirect_limit))
            
            if dto.is_active is not None:
                link.activate() if dto.is_active else link.deactivate()
            
            updated_link = await uow.repository.update(link) # type: ignore

            return LinkDTO.from_entity(updated_link)