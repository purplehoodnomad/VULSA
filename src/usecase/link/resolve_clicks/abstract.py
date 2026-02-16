from abc import ABC, abstractmethod
from usecase.redirect.utils.dto import ClickMetadataDTO


class AbstractResolveClicksUseCase(ABC):
    @abstractmethod
    async def execute(self) -> None:
        raise NotImplementedError