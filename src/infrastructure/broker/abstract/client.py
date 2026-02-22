from abc import ABC, abstractmethod

from infrastructure.broker.abstract.producer import AbstractProducer
from infrastructure.broker.abstract.consumer import AbstractConsumer
from infrastructure.broker.topics import Topic


class AbstractBrokerClient(ABC):
    @abstractmethod
    def init(self, dsn: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_producer(self, **kwargs) -> AbstractProducer:
        raise NotImplementedError()

    @abstractmethod
    async def get_consumer(self, topic: Topic, **kwargs) -> AbstractConsumer:
        raise NotImplementedError()

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError()