from kafka import KafkaProducer as KafkaProducer_

from infrastructure.broker.topics import Topic
from .serializers import serialize


class KafkaProducer:
    def __init__(self, client: KafkaProducer_):
        self._client = client

    async def publish(self, topic: Topic, message: dict) -> None:
        await self._client.send(
            topic=topic,
            value=serialize(message),
        )
