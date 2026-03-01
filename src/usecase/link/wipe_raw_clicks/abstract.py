from abc import ABC, abstractmethod


class AbstractWipeRawClicksUseCase(ABC):
    @abstractmethod
    async def execute(self) -> None:
        raise NotImplementedError()