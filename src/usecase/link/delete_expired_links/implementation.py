from datetime import datetime, timezone, timedelta

from infrastructure.uow.link import AbstractLinkUnitOfWork

from .abstract import AbstractDeleteExpiredLinksUseCase



class DeleteExpiredLinksUseCase(AbstractDeleteExpiredLinksUseCase):
    def __init__(self, uow: AbstractLinkUnitOfWork):
        self.uow = uow

    async def execute(self, delta: timedelta) -> None:
        now = datetime.now(timezone.utc)
        async with self.uow as uow:
            cleanup_list = await uow.link_repo.find_for_cleanup(
                last_used_before=now - delta,
                include_expired=True,
                include_inactive=True,
                include_limit_reached=True
            )

            for link in cleanup_list:
                await uow.link_repo.delete(link)