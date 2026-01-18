from abc import ABC, abstractmethod

from usecase.link.utils.dto import LinkDTO


class AbstractGetAnonymousLinkUseCase(ABC):
    @abstractmethod
    async def execute(self, edit_key: str) -> LinkDTO:
        raise NotImplementedError