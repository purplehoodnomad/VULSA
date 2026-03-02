from asyncio import Lock
import logging

from infrastructure.broker.abstract.client import AbstractBrokerClient
from infrastructure.broker.kafka.producer import KafkaProducer
from infrastructure.broker.kafka.consumer import KafkaConsumer
from infrastructure.broker.kafka.serializers import serialize, deserialize


logger = logging.getLogger(__name__)


class KafkaClient(AbstractBrokerClient):
    def __init__(self) -> None:
        self._bootstrap: str | None = None
        self._consumers: dict[str, KafkaConsumer] = {}
        self._consumer_locks: dict[str, Lock] = {}

    def init(self, dsn: str) -> None:
        if self._bootstrap is None:
            self._bootstrap = dsn


    async def get_consumer(self, topic: str, **kwargs) -> KafkaConsumer:
        if topic in self._consumers:
            return self._consumers[topic]

        lock = self._consumer_locks.setdefault(topic, Lock())
        async with lock:
            if topic in self._consumers:
                return self._consumers[topic]

            if self._bootstrap is None:
                raise RuntimeError("KafkaClient not initialized")
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self._bootstrap,
                key_deserializer=deserialize,
                value_deserializer=deserialize,
                **kwargs
            )
            await consumer.start()
            self._consumers[topic] = consumer
            return consumer

    async def close(self) -> None:
        for consumer in self._consumers.values():
            try:
                await consumer.stop()
            except Exception as e:
                logger.error(e)
        
        self._consumers.clear()
        self._bootstrap = None