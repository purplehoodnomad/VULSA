from domain.link.events import LinkClickEvent
from domain.click_stamp.entity import ClickStamp

from infrastructure.uow.link import AbstractLinkUnitOfWork


class LinkVisitedHandler:
    def __init__(self, uow: AbstractLinkUnitOfWork):
        self._uow = uow

    async def __call__(self, event: LinkClickEvent) -> None:
        async with self._uow as uow:
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
