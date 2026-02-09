from infrastructure.uow.link import AbstractLinkUnitOfWork
from domain.value_objects.link import Short

from usecase.common.event_bus import EventBus
from usecase.link.utils.dto import LinkDTO
from usecase.redirect.utils.dto import ClickMetadataDTO

from .abstract import AbstractLinkRedirectUseCase


class LinkRedirectUseCase(AbstractLinkRedirectUseCase):
    def __init__(
        self,
        uow: AbstractLinkUnitOfWork,
        event_bus: EventBus
    ):
        self.uow = uow
        self.event_bus = event_bus

    async def execute(
        self,
        short: str,
        metadata: ClickMetadataDTO
    ) -> LinkDTO:
        async with self.uow as uow:
            link = await uow.link_repo.get_by_short(Short(short))
            link.consume_redirect(metadata.to_vo_container())
            await uow.link_repo.update(link)
        
        await self.event_bus.publish(link.pull_events())
        return LinkDTO.from_entity(link)