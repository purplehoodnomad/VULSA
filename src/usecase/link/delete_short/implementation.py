from uuid import UUID

from infrastructure.uow.link import AbstractLinkUnitOfWork

from domain.value_objects.common import UserId
from domain.value_objects.link import Short

from domain.link.exceptions import ShortLinkAccessDenied

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
            user = await uow.user_repo.get(UserId(user_id))
            link = await uow.link_repo.get_by_short(Short(short))
            if link.user_id.value != user.user_id.value:
                raise ShortLinkAccessDenied()

            await uow.link_repo.delete(link)