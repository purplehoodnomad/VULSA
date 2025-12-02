from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TEntity = TypeVar("TEntity")
TId = TypeVar("TId")
TCreateDTO = TypeVar("TCreateDTO")
TUpdateDTO = TypeVar("TUpdateDTO")


class AbstractRepository(Generic[TEntity, TId, TCreateDTO, TUpdateDTO], ABC):
    @abstractmethod
    def get(self, entity_id: TId) -> TEntity:
        raise NotImplementedError

    @abstractmethod
    def list(self, *, limit: int = 100, offset: int = 0) -> list[TEntity]:
        raise NotImplementedError

    @abstractmethod
    def create(self, dto: TCreateDTO) -> TEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity_id: TId, dto: TUpdateDTO, wipe: bool) -> TEntity:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: TId) -> None:
        raise NotImplementedError