from abc import ABC, abstractmethod

from usecase.link.utils.dto import LinkDTO


class AbstractLinkRedirectUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        short: str
    ) -> LinkDTO:
        raise NotImplementedError