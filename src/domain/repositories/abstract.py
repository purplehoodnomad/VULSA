from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TEntity = TypeVar("TEntity")
TId = TypeVar("TId")


class AbstractRepository(Generic[TEntity, TId], ABC):
    @abstractmethod
    async def create(self, entity: TEntity) -> TEntity:
        raise NotImplementedError

    # @abstractmethod
    # async def get(self, entity_id: TId) -> TEntity:
    #     raise NotImplementedError

    # @abstractmethod
    # async def list(self, filter: TFilter) -> list[TEntity]:
    #     raise NotImplementedError

    # @abstractmethod
    # async def update(self, entity_id: TId, dto: TUpdateDTO, wipe: bool) -> TEntity:
    #     raise NotImplementedError

    # @abstractmethod
    # async def delete(self, entity_id: TId) -> None:
    #     raise NotImplementedError