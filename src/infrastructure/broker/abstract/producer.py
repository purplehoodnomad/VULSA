from abc import ABC, abstractmethod

from infrastructure.broker.topics import Topic


class AbstractProducer(ABC):
    @abstractmethod
    async def send(self, topic: Topic, message: dict) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError()