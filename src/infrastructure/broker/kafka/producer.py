from aiokafka import AIOKafkaProducer

from infrastructure.broker.abstract.producer import AbstractProducer
from infrastructure.broker.topics import Topic


class KafkaProducer(AbstractProducer):
    def __init__(self, *args, **kwargs):
        self._producer = AIOKafkaProducer(*args, **kwargs)

    async def send(self, topic: Topic, message: dict) -> None:
        return await self._producer.send(topic.value, value=message)

    async def start(self) -> None:
        await self._producer.start()

    async def stop(self) -> None:
        await self._producer.stop()