from abc import ABC, abstractmethod


class AbstractSyncCacheUseCase(ABC):
    @abstractmethod
    async def execute(self) -> None:
        raise NotImplementedError