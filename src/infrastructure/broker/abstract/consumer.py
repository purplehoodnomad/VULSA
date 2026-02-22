from abc import ABC, abstractmethod
from typing import Iterable


class AbstractConsumer(ABC):
    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def getmany(self) -> Iterable:
        raise NotImplementedError()
    
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError()