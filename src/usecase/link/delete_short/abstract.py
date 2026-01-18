from abc import ABC, abstractmethod
from usecase.common.actor import Actor


class AbstractDeleteShortUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        *,
        actor: Actor,
        short: str
    ) -> None:
        raise NotImplementedError