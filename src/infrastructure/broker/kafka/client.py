from asyncio import Lock

from infrastructure.broker.abstract.client import AbstractBrokerClient
from infrastructure.broker.kafka.producer import KafkaProducer
from infrastructure.broker.kafka.consumer import KafkaConsumer
from infrastructure.broker.topics import Topic
from infrastructure.broker.kafka.serializers import serialize, deserialize


class KafkaClient(AbstractBrokerClient):
    def __init__(self) -> None:
        self._bootstrap: str | None = None
        self._producer: KafkaProducer | None = None
        self._consumers: dict[Topic, KafkaConsumer] = {}
        self._producer_lock = Lock()
        self._consumer_locks: dict[Topic, Lock] = {}

    def init(self, dsn: str) -> None:
        if self._bootstrap is None:
            self._bootstrap = dsn


    async def get_producer(self, **kwargs) -> KafkaProducer:
        if self._producer is None:
            async with self._producer_lock:
                if self._producer is None:
                    if self._bootstrap is None:
                        raise RuntimeError("KafkaClient not initialized")
                    producer = KafkaProducer(
                        bootstrap_servers=self._bootstrap,
                        key_serializer=serialize,
                        value_serializer=serialize,
                        **kwargs
                    )
                    await producer.start()
                    self._producer = producer
        return self._producer


    async def get_consumer(self, topic: Topic, **kwargs) -> KafkaConsumer:
        if topic in self._consumers:
            return self._consumers[topic]

        lock = self._consumer_locks.setdefault(topic, Lock())
        async with lock:
            if topic in self._consumers:
                return self._consumers[topic]

            if self._bootstrap is None:
                raise RuntimeError("KafkaClient not initialized")
            consumer = KafkaConsumer(
                topic.value,
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
            except Exception:
                pass
        self._consumers.clear()
        
        if self._producer is not None:
            try:
                await self._producer.stop()
            except Exception:
                pass
            self._producer = None
        self._bootstrap = None