from abc import ABC, abstractmethod
from uuid import UUID

from infrastructure.uow.link import AbstractLinkUnitOfWork

from domain.value_objects.common import UserId
from domain.value_objects.link import Short

from domain.user.exceptions import LinkOwnershipViolation

from .abstract import AbstractDeleteShortUseCase



class PostgresDeleteShortUseCase(AbstractDeleteShortUseCase):
    def __init__(self, uow: AbstractLinkUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        *,
        user_id: UUID,
        short: str
    ) -> None:
        async with self.uow as uow:
            user = await uow.user_repo.get(UserId(user_id)) # type: ignore
            link = await uow.link_repo.get_by_short(Short(short)) # type: ignore
            if link.user_id.value != user.user_id.value:
                raise LinkOwnershipViolation(short=short, user_id=user_id)

            await uow.link_repo.delete(link) # type: ignore