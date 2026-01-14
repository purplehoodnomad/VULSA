from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TEntity = TypeVar("TEntity")


class AbstractRepository(Generic[TEntity], ABC):
    @abstractmethod
    async def create(self, entity: TEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: TEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity: TEntity) -> None:
        raise NotImplementedError