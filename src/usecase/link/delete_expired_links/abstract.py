from abc import ABC, abstractmethod
from datetime import timedelta


class AbstractDeleteExpiredLinksUseCase(ABC):
    @abstractmethod
    async def execute(self, delta: timedelta) -> None:
        raise NotImplementedError