from abc import ABC, abstractmethod
from uuid import UUID


class AbstractDeleteShortUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        *,
        user_id: UUID,
        short: str
    ) -> None:
        raise NotImplementedError