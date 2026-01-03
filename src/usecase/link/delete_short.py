from abc import ABC, abstractmethod
from uuid import UUID

from infrastructure.postgresql.uow.uow import PostgresLinkUoW

from domain.value_objects.common import UserId
from domain.value_objects.link import Short

from domain.link.exceptions import ShortLinkDoesNotExistException
from domain.user.exceptions import LinkOwnershipViolation

from usecase.link.utils.dto import LinkDTO


class AbstractDeleteShortUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        *,
        user_id: UUID,
        short: str
    ) -> None:
        raise NotImplementedError


class PostgresDeleteShortUseCase(AbstractDeleteShortUseCase):
    def __init__(self, uow: PostgresLinkUoW):
        self.uow = uow

    async def execute(
        self,
        *,
        user_id: UUID,
        short: str
    ) -> None:
        async with self.uow as uow:
            user = await uow.user_repository.get(UserId(user_id)) # type: ignore
            link = await uow.repository.get_by_short(Short(short)) # type: ignore
            if link.user_id.value != user.user_id.value:
                raise LinkOwnershipViolation(short=short, user_id=user_id)

            await uow.repository.delete(link) # type: ignore