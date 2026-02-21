from asyncio import sleep
from aiokafka import AIOKafkaConsumer
from datetime import datetime

from .abstract import AbstractResolveClicksUseCase

from infrastructure.uow.link import AbstractLinkUnitOfWork

from usecase.redirect.utils.dto import ClickMetadataDTO
from domain.value_objects.link import Short, ClickStamp


class ResolveClicksUseCase(AbstractResolveClicksUseCase):
    def __init__(
        self,
        uow: AbstractLinkUnitOfWork,
        consumer: AIOKafkaConsumer
    ):
        self.uow = uow
        self.consumer = consumer

    async def execute(self) -> None:
        while True:
            print("working")
            events: list[ClickMetadataDTO] = []
            clicks: set[ClickStamp] = set()
            
            await sleep(5.0)

            res = await self.consumer.getmany()
            for records in res.values():
                for msg in records:
                    if msg.value is None:
                        continue
                    events.append(ClickMetadataDTO(**msg.value))

            unique_shorts = {Short(e.short) for e in events}
            async with self.uow as uow:
                print(type(uow.click_repo))
                link_entities = await uow.link_repo.get_batch(unique_shorts)
                shorts_mapped = {entity.short.value: entity.link_id for entity in link_entities}

            for event in events:
                clicks.add(ClickStamp.create(
                    link_id=shorts_mapped[event.short],
                    short=Short(event.short),
                    timestamp=datetime.fromisoformat(event.timestamp), # type: ignore
                    ip=event.ip,
                    user_agent=event.user_agent,
                    referer=event.referer,
                    request_url=event.request_url
                ))
            try:
                async with self.uow as uow:
                    await uow.click_repo.create_batch(clicks)
                    await self.consumer.commit()
            except Exception as e:
                # TODO: Add handler
                raise
