from typing import AsyncContextManager, Callable

from domain.link.events import LinkClickEvent
from domain.click_stamp.entity import ClickStamp


class LinkVisitedHandler:
    def __init__(self, uow_factory: Callable[[], AsyncContextManager]):
        self._uow_factory = uow_factory

    async def __call__(self, event: LinkClickEvent) -> None:
        async with self._uow_factory() as uow:
            click = ClickStamp.create(
                link_id=event.link_id,
                short=event.short,
                timestamp=event.timestamp,
                ip=event.ip,
                user_agent=event.user_agent,
                referer=event.referer,
                request_url=event.request_url
            )
            await uow.click_repo.create(click)
