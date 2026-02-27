from abc import ABC, abstractmethod


class AbstractProducer(ABC):
    @abstractmethod
    async def send(self, topic: str, message: dict) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError()